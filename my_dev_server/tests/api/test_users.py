import requests
import testtools

from my_dev_server import utils


class TestBase(testtools.TestCase):

    def setUp(self):
        super(TestBase, self).setUp()
        self.url = 'http://localhost:5000'

    def _create_user(self, username, email, password,
                     expected_code=200):
        url = self.url + '/users'
        data = {
            "username": username,
            "email": email,
            "password": password
        }
        user = requests.post(url, json=data)
        self.assertEqual(expected_code, user.status_code)
        return user.json()

    def _delete_user(self, user):
        url = self.url + '/users/%s' % user['id']
        request = requests.delete(url)
        self.assertEqual(200, request.status_code)

    def _create_ssh(self, user,
                    alias='alias',
                    host='',
                    username='username',
                    password='pass'):
        data = {
            "user_id": user['id'],
            "alias": utils.rand_name(alias),
            "host": utils.rand_name(host),
            "username": utils.rand_name(username),
            "password": utils.rand_name(password)
        }
        url = self.url + '/users/%s/ssh' % user['id']
        new_ssh = requests.post(url, json=data)

        self.assertEqual(200, new_ssh.status_code)
        return new_ssh.json()

    def _delete_ssh(self, user, ssh):
        url = self.url + '/users/%s/ssh/%s' % (user['id'], ssh['id'])
        request = requests.delete(url)
        self.assertEqual(200, request.status_code)


class TestUsers(TestBase):

    def test_create_delete_user(self):
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
        user = self._create_user(
            utils.rand_name('user'),
            utils.rand_name('email'),
            utils.rand_name('pass'))
        url = self.url + '/users/%s' % user['id']
        get_user = requests.get(url)

        self.assertEqual(200, get_user.status_code)
        self.assertEqual(user, get_user.json())
        self._delete_user(user)

    def test_create_user_exist_username(self):
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


class TestSsh(TestBase):

    def test_create_delete_ssh(self):
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




