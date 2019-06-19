from sqlalchemy import Column, BigInteger, ForeignKey, Index

from db import Base, db_session


class UserFollowers(Base):
    __tablename__ = 'user_followers'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    follower_id = Column(BigInteger, ForeignKey('users.id'))

    Index('idx_user_id_follower_id', 'user_id', 'follower_id', unique=True)

    def __repr__(self):
        return '<UserFollowers(%r, %r)>' % (self.user_id, self.follower_id)

    def __init__(self, user_id, follower_id):
        self.user_id = user_id
        self.follower_id = follower_id

    def json(self):
        return {"user_followers": {"id": self.id, "user_id": self.user_id, "follower_id": self.follower_id}}

    @classmethod
    def find_by_user_id(cls, user_id):
        return db_session.query(cls).filter_by(user_id=user_id).first()

    @classmethod
    def find_followers_of_user(cls, user_id):
        query_result = db_session.query(cls.follower_id).filter_by(user_id=user_id).all()
        return [result[0] for result in query_result]
