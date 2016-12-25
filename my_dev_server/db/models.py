import sqlalchemy as sql

from my_dev_server.db import base
from my_dev_server import logger

LOG = logger.logger


class User(base.Base):

    __tablename__ = 'users'

    id = sql.Column(sql.Integer, primary_key=True)
    username = sql.Column(sql.String(length=10), nullable=False)
    email = sql.Column(sql.String(length=30), nullable=False)
    password = sql.Column(sql.String(length=30), nullable=False)

    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.username)

    def to_json(self):
        return dict(id=self.id,
                    username=self.username,
                    email=self.email,
                    password=self.password)


class Ssh(base.Base):
    __tablename__ = 'ssh'

    id = sql.Column(sql.Integer, primary_key=True)
    user_id = sql.Column(sql.Integer, sql.ForeignKey('users.id'))
    alias = sql.Column(sql.String(length=30))
    host = sql.Column(sql.String(length=10))
    username = sql.Column(sql.String(length=10))
    password = sql.Column(sql.String(length=30))

    def __init__(self, user_id=None, alias=None, host=None, username=None,
                 password=None):
        self.user_id = user_id
        self.alias = alias
        self.host = host
        self.username = username
        self.password = password

    def __repr__(self):
        return '<SSH %r>' % (self.id)

    def to_json(self):
        return dict(user_id=self.user_id,
                    alias=self.alias,
                    host=self.host)
