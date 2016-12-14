from my_dev_server.db import base


def main():
    # Create the above tables
    base.init_db()
