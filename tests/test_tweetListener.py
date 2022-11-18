import pytest
from app.authenticators import Authenticator
from app.tweetListeners import TweetListener
from pytest import MonkeyPatch


def test_fetch_tweet_valid() -> None:
    assert isinstance(TweetListener(authenticator=Authenticator()).fetch_tweets(), list)


def test_fetch_tweet_invalid(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(Authenticator, "is_authenticated", False)

    with pytest.raises(Exception, match="Authentication did not happen") as exc_info:
        TweetListener(authenticator=Authenticator()).fetch_tweets()

    assert isinstance(exc_info.value.__cause__, UnboundLocalError)


def test_parse_tweets_invalid(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(TweetListener, "fetch_tweets", lambda _: [])
    monkeypatch.setattr(Authenticator, "is_authenticated", lambda _: True)

    assert len(
        TweetListener(
            authenticator=Authenticator()
        ).parse_tweets(
            tweets=TweetListener(
                authenticator=Authenticator()
            ).fetch_tweets())
    ) < 1


def test_parse_tweets_valid(monkeypatch: MonkeyPatch) -> None:
    # TODO: Implement the valid test case
    pass