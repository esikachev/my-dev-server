import sys

from oslo_config import cfg
from oslo_log import log

CONF = cfg.CONF


db_opts = [
    cfg.StrOpt('db_url',
               default='mysql+pymysql://root:r00tme@localhost/my_dev',
               help='Url of DB for connection.')
]

CONF.register_opts(db_opts)

log.register_options(CONF)


def list_opts():
    return {'DEFAULT': db_opts}


def parse_config():
    CONF(project='my-dev-server', default_config_files=sys.argv[2:])
