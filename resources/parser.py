from models import Tweet, User, HashTag


class JSONParser:
    def __init__(self, db_session):
        self.user_id = None
        self.session = db_session

    def persist_user(self, user_json):
        user_payload = user_json[0].copy()
        self.user_id = user_payload['id']   # To ensure that the tweets will also have the user_id

        if not User.find_by_id(user_payload['id']):
            user = User(**user_payload)
            self.session.add(user)
            self.session.flush()
            print("%s added to the session" % str(user))
        else:
            print("User already exists")

    def persist_tweets(self, tweet_list):
        if not self.user_id:
            # rescue user_id from the first tweet retrieved, may not be needed but for later sake
            self.user_id = tweet_list[0]['user']['id']

        tweet_payloads = tweet_list.copy()
        tweet_holder = []
        for payload in tweet_payloads:
            if not Tweet.find_by_id(payload['id']):
                del payload['user']
                tweet_holder.append(Tweet(**payload))

        if tweet_holder:
            self.session.bulk_save_objects(tweet_holder)
            self.session.flush()
            print("tweet_holder saved")
        else:
            print("All Tweets have already been saved in DB")

    def persist_followers(self, followers_json):
        # This is assuming that the followers are optional and that the class would have saved
        # its user_id already
        pass

    def persist_hashtags(self, hashtag_dict):
        for tweet_id, hashtag_list in hashtag_dict.items():
            if not HashTag.find_by_tweet_id(tweet_id):
                hashtag_bag = [HashTag(tweet_id, hashtag['text']) for hashtag in hashtag_list]
                self.session.bulk_save_objects(hashtag_bag)
            else:
                hashtag_bag = [HashTag(tweet_id, hashtag['text']) for hashtag in hashtag_list
                               if not HashTag.find_by_tweet_id_text(tweet_id, hashtag['text'])]
                if hashtag_bag:
                    self.session.bulk_save_objects(hashtag_bag)
                else:
                    print("All HashTags already exist")

        self.session.flush()

    def commit(self):
        self.session.commit()

    @classmethod
    def parse_hashtags_from_tweet(cls, tweet_json):
        tweets = tweet_json.copy()
        tweet_list = []
        hashtags_dict = {}
        for tweet in tweets:
            entities = tweet.pop('entities')
            if entities['hashtags']:
                hashtags_dict[tweet['id']] = entities['hashtags']

            tweet_list.append(tweet)

        return tweet_list, hashtags_dict
