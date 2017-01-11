import sys

from oslo_config import cfg

CONF = cfg.CONF


opts = [
    cfg.BoolOpt('debug', default=False, help='Enable debug for server'),
    cfg.StrOpt('host', default='0.0.0.0', help='Host address for running app'),
    cfg.StrOpt('db_url',
               default='mysql+pymysql://root:r00tme@localhost/my_dev',
               help='Url of DB for connection.'),
    cfg.StrOpt('log_dir',
               default='/var/log/my-dev-server',
               help='Directory name for logs.')
]

CONF.register_opts(opts)


def list_opts():
    return {'DEFAULT': opts}


def parse_config():
    CONF(project='my-dev-server', default_config_files=sys.argv[2:])

