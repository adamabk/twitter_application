from sqlalchemy import (Column,
                        Integer,
                        String,
                        DateTime,
                        Boolean,
                        BigInteger,
                        Index,
                        ForeignKey)
from sqlalchemy.orm import relationship

from db import Base, db_session


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    id_str = Column(String(80))
    name = Column(String(60))   # Capped at 50, just in case String(60)
    screen_name = Column(String(15))
    location = Column(String(30), nullable=True)
    url = Column(String(100), nullable=True)
    description = Column(String(250), nullable=True)
    protected = Column(Boolean)
    verified = Column(Boolean)
    followers_count = Column(Integer)   # It could return 0 if under duress
    friends_count = Column(Integer)   # It could return 0 if under duress
    listed_count = Column(Integer)
    favourites_count = Column(Integer)
    statuses_count = Column(Integer)
    created_at = Column(DateTime)
    profile_banner_url = Column(String(100))
    profile_image_url_https = Column(String(100))
    default_profile = Column(Boolean)
    default_profile_image = Column(Boolean)
    withheld_scope = Column(String(4))

    # all other json keys are deprecated per documentation
    # https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object

    tweets = relationship('Tweet', back_populates='user')

    Index('idx_id', 'id', unique=True)

    def __init__(self, **entries):
        # To ignore certain fields provided in the api itself
        self.__dict__.update(entries)

    def __repr(self):
        return '<User(%r, %r)>' % (self.id, self.name)

    def json(self):
        return {"id": self.id,
                "id_str": self.id_str,
                "name": self.name,
                "tweets": [tweet.json() for tweet in self.tweets],
                "country_withheld": [ct["country_name"] for ct in self.withheld_in_countries]}

    @classmethod
    def find_by_id(cls, _id):
        return db_session.query(cls).filter_by(id=_id).first()
