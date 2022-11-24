from typing import Any

import pytest
from app.authenticators import Authenticator
from app.exceptions import FailedAuthenticationException
from app.tweetListeners import TweetListener
from pytest import MonkeyPatch


@pytest.fixture()
def valid_listener() -> Any:
    yield TweetListener(authenticator=Authenticator())


def test_fetch_tweet_valid(valid_listener) -> None:
    assert isinstance(valid_listener.fetch_tweets(), list)


def test_fetch_tweet_invalid(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(Authenticator, "is_authenticated", False)

    listener = TweetListener(Authenticator())

    with pytest.raises(FailedAuthenticationException, match="Authentication did not happen") as exc_info:
        listener.fetch_tweets()

    assert isinstance(exc_info.value.__cause__, UnboundLocalError)


def test_parse_tweets_valid(valid_listener) -> None:
    with pytest.raises(FileNotFoundError):
        assert len(valid_listener.parse_tweets(
            tweets=valid_listener.fetch_tweets())) >= 1


def test_parse_tweets_invalid(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(TweetListener, "fetch_tweets", lambda _: [])
    monkeypatch.setattr(Authenticator, "is_authenticated", lambda _: True)

    listener = TweetListener(
        authenticator=Authenticator()
    )

    assert len(listener.parse_tweets(tweets=listener.fetch_tweets())) < 1


def test_transform_valid(valid_listener) -> None:
    with pytest.raises(FileNotFoundError):
        assert len(valid_listener.transform(["a.png"])) > 0


def test_transform_invalid(valid_listener) -> None:
    assert len(valid_listener.transform([])) == 0


def test_tablify_invalid(valid_listener) -> None:
    assert valid_listener.tablify([]).shape[0] == 0


def test_tablify_valid() -> None:
    return
