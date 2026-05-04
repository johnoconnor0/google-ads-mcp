# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Publish-readiness hardening (CI workflows, secret scanning, release validation).
- Baseline unit tests for configuration, auth manager, and campaign manager.
- VirusTotal audit workflow and report generation script.
- OSS governance files (`CODE_OF_CONDUCT.md`, issue/PR templates, Dependabot).

### Changed
- Packaging metadata and build targets in `pyproject.toml`.
- Contributor setup and verification instructions.

### Security
- Added automated gitleaks and trufflehog scanning in CI.
- Added `.gitignore` rules for secret-bearing local files and generated artifacts.
