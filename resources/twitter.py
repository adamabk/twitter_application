from base64 import b64encode
from collections import defaultdict

import requests

from models import Tweet, User, HashTag
from db import db_session


class Twitter:
    def __init__(self, consumer_key, consumer_secret):
        self.token_cred = self.__base64_encode(consumer_key, consumer_secret)
        self.base_url = 'https://api.twitter.com'
        self.bearer = None

    def __base64_encode(self, consumer_key, consumer_secret):
        token_credential = bytes('%s:%s' % (consumer_key, consumer_secret), 'utf-8')
        token_credential = b64encode(b'%s' % token_credential)
        return token_credential

    def authenticate(self):
        url = self.base_url + '/oauth2/token'
        headers = {"Authorization": b"Basic %s" % self.token_cred,
                   "Content-Type": "application/x-www-form-urlencoded;charset='UTF-8'",
                   "Accept-Encoding": "gzip"}
        body = {"grant_type": "client_credentials"}

        response = requests.post(url, headers=headers, data=body)
        response.raise_for_status()
        resp_json = response.json()

        if resp_json.get('token_type', False):
            self.bearer = resp_json['access_token']
        else:
            raise RuntimeError("Twitter Authentication Failed - Token Not Found")

    def __call_search(self, endpoint, params):
        if not self.bearer:
            self.authenticate()

        url = self.base_url + endpoint
        headers = {"Authorization": "Bearer %s" % self.bearer,
                   "Accept-Encoding": "gzip"}

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response

    def search_tweets_by_user(self, username, count=5):
        tweet_endpoint = '/1.1/statuses/user_timeline.json'
        params = {"count": count, "screen_name": username}
        response = self.__call_search(tweet_endpoint, params)
        return response.json()

    def search_followers_by_user(self, username, get_all=False):
        followers_endpoint = '/1.1/followers/list.json'
        params = {"screen_name": username}

        if get_all:
            cursor = 0
            followers = defaultdict(list)
            # This would be the way to grab all of the followers.
            # This operation only returns the {"users": [...]}
            while cursor != -1:
                try:
                    response = self.__call_search(followers_endpoint, params)
                    response_json = response.json()
                    followers['users'].extend(response_json['users'])
                    cursor = response_json['next_cursor']
                except requests.exceptions.HTTPError as err:
                    print("Could not finish the task due to - {}".format(err))
            return followers

        response = self.__call_search(followers_endpoint, params)
        return response.json()

    def search_user(self, username):
        user_endpoint = '/1.1/users/lookup.json'
        params = {"screen_name": username}
        response = self.__call_search(user_endpoint, params)
        return response.json()
