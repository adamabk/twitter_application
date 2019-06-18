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

        try:
            response = requests.post(url, headers=headers, data=body)
            resp_json = response.json()
            if resp_json.get('token_type', False):
                self.bearer = resp_json['access_token']
            else:
                raise RuntimeError(
                    "Authentication Failed - please check the consumer_key"\
                    "consumer_credentials\n returned: {}".format(resp_json))

        except requests.exceptions.RequestException as e:
            raise RuntimeError("Twitter Authentication Failed - Request Error: {}".format(e))

    def search_by_user(self, username, count=5):
        url = self.base_url + '/1.1/statuses/user_timeline.json'
        if not self.bearer:
            self.authenticate()

        headers = {"Authorization": "Bearer %s" % self.bearer,
                   "Accept-Encoding": "gzip"}
        params = {"count": count, "screen_name": username}

        try:
            response = requests.get(url, headers=headers, params=params)
            self.parse_and_persist(response)
            return response.json()

        except requests.exceptions.RequestException as e:
            raise RuntimeError("Twitter search by user failed - request Error: {}".format(e))

    def parse_and_persist(self, response):
        response_json = response.json()
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
