from utils.config_manager import AuthConfig, ConfigManager


def test_auth_config_rejects_hyphenated_login_customer_id():
    try:
        AuthConfig(login_customer_id="123-456-7890")
        assert False, "Expected validation failure"
    except ValueError as exc:
        assert "must not contain hyphens" in str(exc)


def test_config_manager_loads_auth_values_from_env(monkeypatch):
    monkeypatch.setenv("GOOGLE_ADS_DEVELOPER_TOKEN", "dev-token")
    monkeypatch.setenv("GOOGLE_ADS_CLIENT_ID", "client-id")
    monkeypatch.setenv("GOOGLE_ADS_CLIENT_SECRET", "client-secret")
    monkeypatch.setenv("GOOGLE_ADS_REFRESH_TOKEN", "refresh-token")

    manager = ConfigManager()
    auth = manager.get_auth_config()

    assert auth.developer_token == "dev-token"
    assert auth.client_id == "client-id"
    assert auth.client_secret == "client-secret"
    assert auth.refresh_token == "refresh-token"


def test_config_manager_validate_reports_missing_oauth_fields(monkeypatch):
    for key in [
        "GOOGLE_ADS_DEVELOPER_TOKEN",
        "GOOGLE_ADS_CLIENT_ID",
        "GOOGLE_ADS_CLIENT_SECRET",
        "GOOGLE_ADS_REFRESH_TOKEN",
    ]:
        monkeypatch.delenv(key, raising=False)

    manager = ConfigManager()
    valid, errors = manager.validate()

    assert not valid
    assert any("developer_token" in err for err in errors)
