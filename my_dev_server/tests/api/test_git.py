import requests

from my_dev_server.tests.api import base
from my_dev_server import utils


class TestGit(base.Base):

    def test_create_delete_git(self):
        """Scenario:
          - create user
          - create new git
          - check that git was created correctly
          - delete git
          - delete user
        """
        user_data, user = self.create_user()

        git_data, git = self.create_git(user['id'])

        self.check_response(git_data, git)

        self.delete_git(user['id'], git['id'])
        self.delete_user(user['id'])
