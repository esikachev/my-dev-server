import requests

from my_dev_server.tests.api import base
from my_dev_server import utils


class TestUsers(base.Base):

    def test_create_delete_user(self):
        """Scenario:
          - create user
          - delete user
        """
        user = self.create_user()
        self.delete_user(user['id'])

    def test_get_user(self):
        """Scenario:
          - create user
          - get user
          - delete user
        """
        user = self.create_user()
        get_user = self.get_user(user['id'])
        
        self.check_response(user, get_user)

        self.delete_user(user['id'])

    def test_get_non_existing_user(self):
        """Scenario:
          - Try to get non existing user
          - check that status code correct (404)
        """
        self.get_user('11111', expected_code=404)

    def test_create_user_exist_username(self):
        """Scenario:
          - create user
          - Try to create user with existing username
          - Check that exit code correct (409)
          - delete user
        """
        user = self.create_user('username')
        self.create_user('username', expected_code=409)
        self.delete_user(user)

    def test_create_user_without_username(self):
        """Scenario:
          - Try to create user without username
          - Check that exit code correct (400)
          - Check that error message is correct
        """
        self.create_user(username=None, error_msg='Please provide: username, '
                                                  'password and email')

    def test_create_user_not_correct_creds(self):
        """Scenario:
          - create user with not correct username
          - check that exit code and message are correct
          - create user with not correct password
          - check that exit code and message are correct
          - create user with not correct email
          - check that exit code and message are correct
        """
        self.create_user(username=utils.rand_name(length=2),
                         error_msg='Username len required > 2',
                         expected_code=411)

        self.create_user(password=utils.rand_name(length=4),
                         error_msg='Password len required > 5',
                         expected_code=411)

        self.create_user(email=utils.rand_name(length=2),
                         error_msg='Email len required > 4',
                         expected_code=411)

    def test_create_user_exist_email(self):
        """Scenario:
          - create user
          - Try to create user with existing email
          - Check that exit code correct (409)
          - delete user
        """
        user = self.create_user(email='email')
        self.create_user(email='email', expected_code=409)
        self.delete_user(user['id'])

    def check_response(self, data, user):
        self.assertEqual(data['username'], user['username'])
        self.assertEqual(data['email'], user['email'])
        self.assertEqual(data['password'], user['password'])
