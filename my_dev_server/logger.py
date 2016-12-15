import functools
import logging
import os
import traceback

from oslo_config import cfg

from my_dev_server import config

config.parse_config()
CONF = cfg.CONF


if not os.path.exists(CONF.log_dir):
    os.makedirs(CONF.log_dir)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s %(filename)s:'
                    '%(lineno)d -- %(message)s',
                    filename=os.path.join(CONF.log_dir, 'my-dev-server.log'),
                    filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s %(filename)s:'
                              '%(lineno)d -- %(message)s')
console.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(console)


def debug(logger):
    def wrapper(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            logger.debug(
                "Calling: {} with args: {} {}".format(
                    func.__name__, args, kwargs
                )
            )
            try:
                result = func(*args, **kwargs)
                logger.debug(
                    "Done: {} with result: {}".format(func.__name__, result))
            except BaseException as e:
                logger.error(
                    '{func} raised: {exc!r}\n'
                    'Traceback: {tb!s}'.format(
                        func=func.__name__, exc=e, tb=traceback.format_exc()))
                raise
            return result
        return wrapped
    return wrapper


logwrap = debug(logger)

