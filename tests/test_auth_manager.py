from utils.auth_manager import GoogleAdsAuthManager, AuthenticationError


class _DummyClient:
    pass


def test_initialize_oauth_stores_client(monkeypatch):
    manager = GoogleAdsAuthManager()

    class _TokenManagerStub:
        def __init__(self, *args, **kwargs):
            pass

        def validate_token(self):
            return True

    def _fake_loader(credentials):
        assert credentials["developer_token"] == "dev"
        return _DummyClient()

    monkeypatch.setattr("utils.auth_manager.TokenManager", _TokenManagerStub)
    monkeypatch.setattr(
        "utils.auth_manager.GoogleAdsClient.load_from_dict", _fake_loader
    )

    client_key = manager.initialize_oauth(
        developer_token="dev",
        client_id="cid",
        client_secret="csecret",
        refresh_token="rtoken",
    )

    assert client_key == "default"
    assert isinstance(manager.get_client(), _DummyClient)


def test_initialize_oauth_raises_on_invalid_token(monkeypatch):
    manager = GoogleAdsAuthManager()

    class _TokenManagerStub:
        def __init__(self, *args, **kwargs):
            pass

        def validate_token(self):
            return False

    monkeypatch.setattr("utils.auth_manager.TokenManager", _TokenManagerStub)

    try:
        manager.initialize_oauth("dev", "cid", "sec", "rtok")
        assert False, "Expected AuthenticationError"
    except AuthenticationError as exc:
        assert "Invalid refresh token" in str(exc)
