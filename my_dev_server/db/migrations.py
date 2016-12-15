from my_dev_server.db import base
from my_dev_server import logger

LOG = logger.logger


def main():
    # Create the above tables
    base.init_db()
