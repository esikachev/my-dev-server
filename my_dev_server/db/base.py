from oslo_config import cfg
import sqlalchemy as sql

from my_dev_server import config

config.parse_config()

CONF = cfg.CONF


class Connect(object):
    def __init__(self):
        '''Returns a connection and a metadata object'''

        # We connect with the help of the DB URL
        url = CONF.db_url

        # The return value of create_engine() is our connection object
        self.connection = sql.create_engine(url)

        # We then bind the connection to MetaData()
        self.metadata = sql.MetaData(bind=self.connection, reflect=True)
