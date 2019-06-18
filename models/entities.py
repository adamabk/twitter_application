from sqlalchemy import Column, String, BigInteger, ForeignKey, Index
from sqlalchemy.orm import relationship

from db import Base, db_session


class HashTag(Base):
    __tablename__ = 'hashtags'

    id = Column(BigInteger, primary_key=True)
    tweet_id = Column(BigInteger, ForeignKey('tweets.id'), nullable=False)
    text = Column(String(100))

    tweet = relationship('Tweet', back_populates='hashtags')

    Index('idx_id_tweet_id', 'id', 'tweet_id', unique=True)

    def __repr__(self):
        return '<HashTag(%r, %r)>' % (self.id, self.tweet_id)

    def __init__(self, tweet_id, text):
        self.tweet_id = tweet_id
        self.text = text

    def json(self):
        return {"hashtag": {"id": self.id, "tweet_id": self.tweet_id, "text": self.text}}

    @classmethod
    def save_hashtag(cls, tweet, hashtags):
        for hashtag in hashtags:
            tweet.hashtags.append(HashTag(tweet.id, hashtag['text']))

        return tweet


# Entities hold all of the extra information regarding media, polls, and symbols
# but for the sake of this project, will not continue modeling the data
