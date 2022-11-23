import pytest
from app.authenticators import Authenticator
from app.tweetListeners import TweetListener
from pytest import MonkeyPatch


def test_fetch_tweet_valid() -> None:
    assert isinstance(TweetListener(
        authenticator=Authenticator()).fetch_tweets(), list)


def test_fetch_tweet_invalid(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(Authenticator, "is_authenticated", False)

    with pytest.raises(Exception, match="Authentication did not happen") as exc_info:
        TweetListener(authenticator=Authenticator()).fetch_tweets()

    assert isinstance(exc_info.value.__cause__, UnboundLocalError)


def test_parse_tweets_invalid(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(TweetListener, "fetch_tweets", lambda _: [])
    monkeypatch.setattr(Authenticator, "is_authenticated", lambda _: True)

    listener = TweetListener(
        authenticator=Authenticator()
    )

    assert len(listener.parse_tweets(tweets=listener.fetch_tweets())) < 1


def test_parse_tweets_valid(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(Authenticator, "is_authenticated", lambda _: True)

    listener = TweetListener(authenticator=Authenticator())

    with pytest.raises(FileNotFoundError) as exc_info:
        assert len(listener.parse_tweets(tweets=listener.fetch_tweets())) >= 1


def test_transform_valid(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(Authenticator, "is_authenticated", lambda _: True)

    listener = TweetListener(authenticator=Authenticator())

    with pytest.raises(FileNotFoundError):
        assert len(listener.transform(["a.png"])) > 0


def test_transform_invalid(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(Authenticator, "is_authenticated", lambda _: True)

    listener = TweetListener(authenticator=Authenticator())

    assert len(listener.transform([])) == 0
