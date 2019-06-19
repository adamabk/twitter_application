from sqlalchemy import (Column,
                        Integer,
                        String,
                        DateTime,
                        Boolean,
                        JSON,
                        BigInteger,
                        ForeignKey,
                        Index)
from sqlalchemy.orm import relationship

from db import Base, db_session


class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(BigInteger, primary_key=True)
    id_str = Column(String(80))
    user_id = Column(BigInteger, ForeignKey('users.id'))
    created_at = Column(DateTime, nullable=False)
    text = Column(String(140))   # Tweeter limits their tweet to 140 chars
    truncated = Column(Boolean)
    source = Column(String(200))
    geo = Column(String(100), nullable=True)
    coordinates = Column(JSON, nullable=True)
    place = Column(JSON, nullable=True)
    contributors = Column(String(10), nullable=True)
    is_quote_status = Column(Boolean)
    retweet_count = Column(Integer)
    favorite_count = Column(Integer)
    favorited = Column(Boolean)
    retweeted = Column(Boolean)
    possibly_sensitive = Column(Boolean)
    lang = Column(String(10))   # Per BCP47 Appendix A.
    in_reply_to_status_id = Column(BigInteger, nullable=True)
    in_reply_to_status_id_str = Column(String(80), nullable=True)
    in_reply_to_user_id = Column(BigInteger, nullable=True)
    in_reply_to_user_id_str = Column(String(80), nullable=True)
    in_reply_to_screen_name = Column(String(60), nullable=True)

    hashtags = relationship('HashTag', back_populates='tweet')
    user = relationship('User', back_populates='tweets')
    # entities = relationship('Hashtag')

    Index('idx_id_user_id', 'id', 'user_id', unique=True)

    def __repr__(self):
        return '<Tweet(%r)>' % (self.id)

    def __init__(self, **entries):
        self.__dict__.update(entries)

    def json(self):
        return {"tweet": {"id": self.id,
                          "id_str": self.id_str,
                          "created_at": self.created_at,
                          "text": self.text,
                          "truncated": self.truncated,
                          "source": self.source,
                          "coordinates": self.coordinates,
                          "place": self.place,
                          "is_quote_status": self.is_quote_status,
                          "retweet_count": self.retweet_count,
                          "favorite_count": self.favorite_count,
                          "favorited": self.favorited,
                          "retweeted": self.retweeted,
                          "possibly_sensitive": self.possibly_sensitive,
                          "lang": self.lang,
                          "user_id": self.user_id}}

    @classmethod
    def find_by_id(cls, _id):
        return db_session.query(cls).filter_by(id=_id).first()
