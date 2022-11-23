import pytest
import tweepy
from app.authenticators import Authenticator
from app.exceptions import InvalidCredentialsException
from pytest import MonkeyPatch


def test_authenticator() -> None:
    assert Authenticator().is_authenticated == True


def test_failed_authentication() -> None:
    with pytest.raises(InvalidCredentialsException, match="Unauthorised/Invalid credentials") as exc_info:
        Authenticator(
            api_key="a", api_key_secret="b", access_token="c", access_token_secret="d"
        )

    assert isinstance(exc_info.value.__cause__, tweepy.errors.Unauthorized)


def test_get_api(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(Authenticator, "is_authenticated", lambda _: True)

    assert isinstance(Authenticator().get_api(), tweepy.API)
