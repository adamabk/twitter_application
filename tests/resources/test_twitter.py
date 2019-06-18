import requests

from resources import Twitter
from tests.resources.mocked_responses import mocked_request_get, mocked_request_post


twitter_client = Twitter("consumer_key", "consumer_secret")

def test_correct_authenticate(monkeypatch):
    monkeypatch.setattr(requests, "post", mocked_request_post('success'))
    twitter_client.authenticate()
    assert twitter_client.bearer == "your_token"


def test_failed_request_authenticate(monkeypatch):
    pass


def test_failed_auth_code_authenticate(monkeypatch):
    pass


def test_correct_search_by_user(monkeypatch):
    pass


def test_no_username_search_by_user(monkeypatch):
    pass


def test_incorrect_search_by_user(monkeypatch):
    pass
