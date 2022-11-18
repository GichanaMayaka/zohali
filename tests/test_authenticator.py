import pytest
import tweepy
from app.authenticators import Authenticator


def test_authenticator() -> None:
    assert Authenticator().authentication_status == True


def test_failed_authentication() -> None:
    with pytest.raises(Exception, match="Unauthorised credentials") as exc_info:
        Authenticator(
            api_key="a", api_key_secret="b", access_token="c", access_token_secret="d"
        )

    assert isinstance(exc_info.value.__cause__, tweepy.errors.Unauthorized)


def test_get_api() -> None:
    assert isinstance(Authenticator().get_api(), tweepy.API)
