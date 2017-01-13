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

    def _get_user(self, user, expected_code=200):
        url = self.url + '/users/%s' % user['id']
        get_user = requests.get(url)
        self.assertEqual(expected_code, get_user.status_code)
        return get_user.json()

    def _delete_user(self, user):
        url = self.url + '/users/%s' % user['id']
        request = requests.delete(url)
        self.assertEqual(200, request.status_code)

    def _create_ssh(self, user,
                    alias='alias',
                    host='',
                    username='username',
                    password='pass',
                    expected_code=200):
        data = {
            "user_id": user['id'],
            "alias": utils.rand_name(alias),
            "host": utils.rand_name(host),
            "username": utils.rand_name(username),
            "password": utils.rand_name(password)
        }
        url = self.url + '/users/%s/ssh' % user['id']
        new_ssh = requests.post(url, json=data)

        self.assertEqual(expected_code, new_ssh.status_code)
        return new_ssh.json()

    def _delete_ssh(self, user, ssh):
        url = self.url + '/users/%s/ssh/%s' % (user['id'], ssh['id'])
        request = requests.delete(url)
        self.assertEqual(200, request.status_code)


class TestUsers(TestBase):

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
        url = self.url + '/users'
        data = {
            "username": 'un',
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
            "password": 'pass'
        }
        message = 'Password len required > 5'
        user = requests.post(url, json=data).json()
        self.assertEqual(411, user['status_code'])
        self.assertEqual(message, user['message'])

        data = {
            "username": utils.rand_name('username'),
            "email": 'un',
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

    def test_create_exist_ssh(self):
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