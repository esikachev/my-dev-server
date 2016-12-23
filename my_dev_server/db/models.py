from datetime import datetime
import sqlalchemy as sql

from my_dev_server.db import base
from my_dev_server import logger

LOG = logger.logger


class User(base.Base):

    __tablename__ = 'users'

    id = sql.Column(sql.Integer, primary_key=True)
    username = sql.Column(sql.String(length=10))
    email = sql.Column(sql.String(length=30))
    registered_on = db.Column('registered_on' , db.DateTime)

    def __init__(self, username=None, email=None):
        self.username = username
        self.email = email
        self.registered_on = datetime.utcnow()

    def __repr__(self):
        return '<User %r>' % (self.username)

    def to_json(self):
        return dict(id=self.id,
                    username=self.username,
                    email=self.email)


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
