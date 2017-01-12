import requests
import testtools

from my_dev_server import utils


class TestUsers(testtools.TestCase):

    def setUp(self):
        super(TestUsers, self).setUp()
        self.url = 'http://localhost:5000%s'

    def _create_user(self, username, email, password,
                     expected_code=200):
        url = self.url % '/users'
        data = {
            "username": username,
            "email": email,
            "password": password
        }
        user = requests.post(url, json=data)
        self.assertEqual(expected_code, user.status_code)
        return user

    def _delete_user(self, user):
        url = self.url % ('/users/%s' % user['id'])
        request = requests.delete(url)
        self.assertEqual(200, request.status_code)

    def test_create_delete_user(self):
        url = self.url % '/users'
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
        url = self.url % ('/users/%s' % user['id'])
        request = requests.delete(url)
        self.assertEqual(200, request.status_code)

    def test_get_user(self):
        user = self._create_user(
            utils.rand_name('user'),
            utils.rand_name('email'),
            utils.rand_name('pass')).json()
        url = self.url % ('/users/%s' % user['id'])
        get_user = requests.get(url)

        self.assertEqual(200, get_user.status_code)
        self.assertEqual(user, get_user.json())
        self._delete_user(user)

    def test_create_delete_ssh(self):
        user = self._create_user(
            utils.rand_name('user'),
            utils.rand_name('email'),
            utils.rand_name('pass')).json()
        data = {
            "user_id": user['id'],
            "alias": 'test_alias',
            "host": '10.10.0.1',
            "username": 'test_username',
            "password": "testp_pass"
        }
        url = self.url % ('/users/%s/ssh' % user['id'])
        new_ssh = requests.post(url, json=data)

        self.assertEqual(200, new_ssh.status_code)
        new_ssh = new_ssh.json()
        self.assertEqual(data['user_id'], new_ssh['user_id'])
        self.assertEqual(data['alias'], new_ssh['alias'])
        self.assertEqual(data['host'], new_ssh['host'])
        self.assertEqual(data['username'], new_ssh['username'])

        url = self.url % ('/users/%s/ssh/%s' % (
            user['id'],
            new_ssh['id']))
        request = requests.delete(url)
        self.assertEqual(200, request.status_code)
        self._delete_user(user)
