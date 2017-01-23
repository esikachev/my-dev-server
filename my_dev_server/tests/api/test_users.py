import requests

from my_dev_server.tests.api import base
from my_dev_server import utils


class TestUsers(base.Base):

    def test_create_delete_user(self):
        """Scenario:
          - create user
          - check that user created successfully
          - delete user
          - check that user deleted
        """
        url = self.url + '/users'
        data = {
            "username": utils.rand_name('user'),
            "email": utils.rand_name('email'),
            "password": utils.rand_name('pass')
        }
        user = requests.post(url, json=data)
        self.assertEqual(200, user.status_code)
        user = user.json()
        self.assertEqual(data['username'], user['username'])
        self.assertEqual(data['email'], user['email'])
        self.assertEqual(data['password'], user['password'])
        url = self.url + '/users/%s' % user['id']
        request = requests.delete(url)
        self.assertEqual(200, request.status_code)

    def test_get_user(self):
        """Scenario:
          - create user
          - get user
          - delete user
        """
        user = self._create_user(
            utils.rand_name('user'),
            utils.rand_name('email'),
            utils.rand_name('pass'))
        url = self.url + '/users/%s' % user['id']
        get_user = requests.get(url)

        self.assertEqual(200, get_user.status_code)
        self.assertEqual(user, get_user.json())
        self._delete_user(user)

    def test_get_non_existing_user(self):
        """Scenario:
          - Try to get non existing user
          - check that status code correct (404)
        """
        fake_user = {
            "id": utils.rand_name('123'),
            "username": utils.rand_name('username'),
            "email": utils.rand_name('email'),
            "password": utils.rand_name('pass')
        }
        self._get_user(fake_user, expected_code=404)

    def test_create_user_exist_username(self):
        """Scenario:
          - create user
          - Try to create user with existing username
          - Check that exit code correct (400)
          - delete user
        """
        user = self._create_user(
            'username',
            utils.rand_name('email'),
            utils.rand_name('pass'))
        self._create_user(
            'username',
            utils.rand_name('email'),
            utils.rand_name('pass'),
            expected_code=400)
        self._delete_user(user)

    def test_create_user_without_username(self):
        """Scenario:
          - Try to create user without username
          - Check that exit code correct (400)
          - Check that error message is correct
        """
        url = self.url + '/users'
        data = {
            "email": utils.rand_name('email'),
            "password": utils.rand_name('pass')
        }
        message = 'Please provide: username, password and email'
        user = requests.post(url, json=data).json()
        self.assertEqual(400, user['status_code'])
        self.assertEqual(message, user['message'])

    def test_create_user_not_correct_creds(self):
        """Scenario:
          - create user with not correct username
          - check that exit code and message are correct
          - create user with not correct password
          - check that exit code and message are correct
          - create user with not correct email
          - check that exit code and message are correct
        """
        url = self.url + '/users'
        data = {
            "username": utils.rand_name(length=2),
            "email": utils.rand_name('email'),
            "password": utils.rand_name('pass')
        }
        message = 'Username len required > 2'
        user = requests.post(url, json=data).json()
        self.assertEqual(411, user['status_code'])
        self.assertEqual(message, user['message'])

        data = {
            "username": utils.rand_name('username'),
            "email": utils.rand_name('email'),
            "password": utils.rand_name(length=4)
        }
        message = 'Password len required > 5'
        user = requests.post(url, json=data).json()
        self.assertEqual(411, user['status_code'])
        self.assertEqual(message, user['message'])

        data = {
            "username": utils.rand_name('username'),
            "email": utils.rand_name(length=2),
            "password": utils.rand_name('password')
        }
        message = 'Email len required > 4'
        user = requests.post(url, json=data).json()
        self.assertEqual(411, user['status_code'])
        self.assertEqual(message, user['message'])

    def test_create_user_exist_email(self):
        """Scenario:
          - create user
          - Try to create user with existing email
          - Check that exit code correct (400)
          - delete user
        """
        user = self._create_user(
            utils.rand_name('username'),
            'email',
            utils.rand_name('pass'))
        self._create_user(
            utils.rand_name('username'),
            'email',
            utils.rand_name('pass'),
            expected_code=400)
        self._delete_user(user)
