from base64 import b64encode

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

    def search_by_user(self, username, count=5):
        url = self.base_url + '/1.1/statuses/user_timeline.json'
        if not self.bearer:
            self.authenticate()

        headers = {"Authorization": "Bearer %s" % self.bearer,
                   "Accept-Encoding": "gzip"}
        params = {"count": count, "screen_name": username}

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def parse_and_persist(self, response_json):
        user_payload = response_json[0]['user']
        if not User.find_by_id(user_payload['id']):
            user = User(**user_payload)
            db_session.add(user)

        for payload in response_json:
            if not Tweet.find_by_id(payload['id']):
                entities_json = payload.pop('entities')
                hashtags = entities_json['hashtags']

                tweet = Tweet.save_tweet(payload)
                if hashtags:
                    tweet = HashTag.save_hashtag(tweet, hashtags)

                db_session.add(tweet)

        db_session.commit()
