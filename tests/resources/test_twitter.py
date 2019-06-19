import requests
from requests.exceptions import HTTPError

import pytest

from resources import Twitter
from tests.resources.mocked_responses import mocked_request_post


@pytest.fixture
def twitter_client_factory():
    twitter_client = Twitter("consumer_key", "consumer_secret")
    return twitter_client

# Testing the token set for the self.bearer
def test_correct_authenticate(twitter_client_factory, monkeypatch):
    monkeypatch.setattr(requests, "post", mocked_request_post('success'))
    twitter_client_factory.authenticate()
    assert twitter_client_factory.bearer == "your_token"


# Test to see if the token was grabbed even if the requests returned `ok`
def test_token_not_found_request_authenticate(twitter_client_factory, monkeypatch):
    with pytest.raises(RuntimeError):
        monkeypatch.setattr(requests, "post", mocked_request_post('invalid_token'))
        twitter_client_factory.authenticate()


def test_failed_auth_code_authenticate(twitter_client_factory, monkeypatch):
    with pytest.raises(HTTPError):
        monkeypatch.setattr(requests, "post", mocked_request_post('fail'))
        twitter_client_factory.authenticate()
