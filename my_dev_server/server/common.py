from oslo_config import cfg

from my_dev_server.server import exceptions
from my_dev_server import config
from my_dev_server import logger

config.parse_config()
CONF = cfg.CONF

LOG = logger.logger


def check_user_correct(username=None, email=None, password=None):

    if username and (len(username) < CONF.MINIMAL_USERNAME_LEN):
        err_message = "Username len required > %s" % CONF.MINIMAL_USERNAME_LEN
        LOG.debug(err_message)
        raise exceptions.LengthRequired(err_message)

    if email and (len(email) < CONF.MINIMAL_EMAIL_LEN):
        err_message = "Email len required > %s" % CONF.MINIMAL_EMAIL_LEN
        LOG.debug(err_message)
        raise exceptions.LengthRequired(err_message)

    if password and (len(password) < CONF.MINIMAL_PASSWORD_LEN):
        err_message = "Password len required > %s" % CONF.MINIMAL_PASSWORD_LEN
        LOG.debug(err_message)
        raise exceptions.LengthRequired(err_message)
