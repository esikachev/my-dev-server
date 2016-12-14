import sqlalchemy as sql


from my_dev_server.db import base

db = base.Connect()

users = sql.Table('users', db.metadata,
                  sql.Column('id', sql.Integer, primary_key=True),
                  sql.Column('username', sql.String(length=15)),
                  sql.Column('email', sql.String(length=30)),
                  sql.Column('ssh_id', sql.Integer,
                             sql.ForeignKey('ssh.id')),
                  extend_existing=True
                  )

ssh = sql.Table('ssh', db.metadata,
                sql.Column('id', sql.Integer, primary_key=True),
                sql.Column('user_id', sql.String(length=15)),
                sql.Column('alias', sql.String(length=30)),
                sql.Column('host', sql.String(length=10)),
                sql.Column('username', sql.String(length=10)),
                sql.Column('password', sql.String(length=30)),
                sql.Column('user_id', sql.String(length=30)),
                extend_existing=True
                )


def main():
    # Create the above tables
    db.metadata.create_all(db.connection)
