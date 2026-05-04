import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";

const API_KEY = process.env.VT_API_KEY;
if (!API_KEY) {
  throw new Error("VT_API_KEY is required");
}

const repoRoot = process.cwd();
const vtDir = path.join(repoRoot, ".virustotal");
await fs.mkdir(vtDir, { recursive: true });

const candidateFiles = [
  "google_ads_mcp.py",
  "requirements.txt",
  "pyproject.toml",
  "README.md",
  "SECURITY.md",
  ".github/workflows/ci.yml",
  ".github/workflows/secret-scan.yml",
  ".github/workflows/release-check.yml",
];

async function hashFile(filePath) {
  const buffer = await fs.readFile(filePath);
  return crypto.createHash("sha256").update(buffer).digest("hex");
}

async function queryHash(sha256) {
  const url = `https://www.virustotal.com/api/v3/files/${sha256}`;
  const response = await fetch(url, {
    headers: {
      "x-apikey": API_KEY,
    },
  });

  if (response.status === 404) {
    return { found: false, sha256 };
  }
  if (!response.ok) {
    const text = await response.text();
    throw new Error(`VirusTotal query failed (${response.status}): ${text}`);
  }

  const data = await response.json();
  const stats = data?.data?.attributes?.last_analysis_stats ?? {};
  return {
    found: true,
    sha256,
    harmless: stats.harmless ?? 0,
    suspicious: stats.suspicious ?? 0,
    malicious: stats.malicious ?? 0,
    undetected: stats.undetected ?? 0,
    timeout: stats.timeout ?? 0,
    typeUnsupported: stats["type-unsupported"] ?? 0,
    vtPermalink: `https://www.virustotal.com/gui/file/${sha256}`,
  };
}

const results = [];
for (const relPath of candidateFiles) {
  const absPath = path.join(repoRoot, relPath);
  try {
    await fs.access(absPath);
  } catch {
    continue;
  }

  const sha256 = await hashFile(absPath);
  const vt = await queryHash(sha256);
  results.push({ file: relPath, ...vt });
}

const now = new Date().toISOString();
const report = {
  generatedAt: now,
  scannedFiles: results.length,
  results,
};

await fs.writeFile(
  path.join(vtDir, "latest.json"),
  JSON.stringify(report, null, 2) + "\n",
  "utf8"
);

const flagged = results.filter((r) => r.found && (r.malicious > 0 || r.suspicious > 0));

const securityPath = path.join(repoRoot, "SECURITY.md");
const securityContent = await fs.readFile(securityPath, "utf8");
const markerStart = "<!-- VIRUSTOTAL-AUDIT:START -->";
const markerEnd = "<!-- VIRUSTOTAL-AUDIT:END -->";

const lines = [];
lines.push(markerStart);
lines.push("## VirusTotal Audit");
lines.push("");
lines.push(`Last updated: ${now}`);
lines.push("");
if (results.length === 0) {
  lines.push("No candidate files were scanned.");
} else {
  lines.push("| File | SHA256 | Status | Link |");
  lines.push("| --- | --- | --- | --- |");
  for (const row of results) {
    const status = !row.found
      ? "Not present in VirusTotal"
      : row.malicious > 0
        ? `Malicious detections: ${row.malicious}`
        : row.suspicious > 0
          ? `Suspicious detections: ${row.suspicious}`
          : "No malicious/suspicious detections";
    const link = row.found ? `[Report](${row.vtPermalink})` : "n/a";
    lines.push(`| ${row.file} | ${row.sha256} | ${status} | ${link} |`);
  }
}
lines.push("");
lines.push("Raw report is stored in `.virustotal/latest.json`.");
lines.push(markerEnd);

const block = lines.join("\n");
let nextContent;
if (securityContent.includes(markerStart) && securityContent.includes(markerEnd)) {
  const regex = new RegExp(`${markerStart}[\\s\\S]*?${markerEnd}`, "m");
  nextContent = securityContent.replace(regex, block);
} else {
  nextContent = `${securityContent.trimEnd()}\n\n${block}\n`;
}

await fs.writeFile(securityPath, nextContent, "utf8");

if (flagged.length > 0) {
  throw new Error(`VirusTotal flagged ${flagged.length} file(s).`);
}
