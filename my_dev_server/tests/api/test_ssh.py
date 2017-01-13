import requests

from my_dev_server.tests.api.base import TestBase
from my_dev_server import utils


class TestSsh(TestBase):

    def test_create_delete_ssh(self):
        """Scenario:
          - create user
          - create new ssh
          - check that ssh was created correctly
          - delete ssh
          - delete user
        """
        user = self._create_user(
            utils.rand_name('user'),
            utils.rand_name('email'),
            utils.rand_name('pass'))
        data = {
            "user_id": user['id'],
            "alias": utils.rand_name('alias'),
            "host": utils.rand_name(''),
            "username": utils.rand_name('username'),
            "password": utils.rand_name('pass')
        }
        url = self.url + '/users/%s/ssh' % user['id']
        new_ssh = requests.post(url, json=data)

        self.assertEqual(200, new_ssh.status_code)
        new_ssh = new_ssh.json()
        self.assertEqual(data['user_id'], new_ssh['user_id'])
        self.assertEqual(data['alias'], new_ssh['alias'])
        self.assertEqual(data['host'], new_ssh['host'])
        self.assertEqual(data['username'], new_ssh['username'])

        url = self.url + '/users/%s/ssh/%s' % (
            user['id'],
            new_ssh['id'])
        request = requests.delete(url)
        self.assertEqual(200, request.status_code)
        self._delete_user(user)

    def test_get_ssh(self):
        """Scenario:
          - create user
          - create new ssh
          - get ssh
          - check that ssh is correct
          - delete ssh
          - delete user
        """
        user = self._create_user(
            utils.rand_name('user'),
            utils.rand_name('email'),
            utils.rand_name('pass'))
        ssh = self._create_ssh(user)
        url = self.url + '/users/%s/ssh/%s' % (user['id'], ssh['id'])
        get_ssh = requests.get(url)
        self.assertEqual(200, get_ssh.status_code)
        get_ssh = get_ssh.json()
        self.assertEqual(ssh['id'], get_ssh['id'])
        self.assertEqual(ssh['alias'], get_ssh['alias'])
        self.assertEqual(ssh['username'], get_ssh['username'])
        self.assertEqual(ssh['host'], get_ssh['host'])

        self._delete_ssh(user, ssh)
        self._delete_user(user)

    def test_create_exist_ssh(self):
        """Scenario:
          - create user
          - create ssh
          - try to create ssh with same data
          - check that 2'nd ssh was not created
          - delete ssh
          - delete user
        """
        user = self._create_user(
            utils.rand_name('user'),
            utils.rand_name('email'),
            utils.rand_name('pass'))
        data = {
            "user_id": user['id'],
            "alias": utils.rand_name('alias'),
            "host": utils.rand_name(''),
            "username": utils.rand_name('username'),
            "password": utils.rand_name('pass')
        }
        url = self.url + '/users/%s/ssh' % user['id']
        new_ssh = requests.post(url, json=data)

        self.assertEqual(200, new_ssh.status_code)
        exist_ssh = requests.post(url, json=data)
        self.assertEqual(400, exist_ssh.status_code)
        self._delete_ssh(user, new_ssh.json())
        self._delete_user(user)
