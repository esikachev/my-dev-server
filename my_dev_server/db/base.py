from oslo_config import cfg
import sqlalchemy as sql
from sqlalchemy import orm
from sqlalchemy.ext import declarative as dec

from my_dev_server import config

config.parse_config()

CONF = cfg.CONF


url = CONF.db_url

engine = sql.create_engine(url)

session = orm.scoped_session(orm.sessionmaker(autocommit=False,
                                              autoflush=False,
                                              bind=engine))
Base = dec.declarative_base()
Base.query = session.query_property()


def init_db():
    import my_dev_server.db.models
    Base.metadata.create_all(bind=engine)
