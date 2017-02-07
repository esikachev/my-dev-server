import requests
import testtools

from my_dev_server import utils


class Base(testtools.TestCase):

    def setUp(self):
        super(Base, self).setUp()
        self.url = 'http://localhost:5000'

    def _create_user(self, username, email, password,
                     expected_code=200):
        url = self.url + '/users'
        data = {
            "username": username,
            "email": email,
            "password": password
        }
        user = self.post(url, data)
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
            "ssh_username": utils.rand_name(username),
            "ssh_password": utils.rand_name(password)
        }
        url = self.url + '/users/%s/ssh' % user['id']
        new_ssh = self.post(url, json=data)

        self.assertEqual(expected_code, new_ssh.status_code)
        return new_ssh.json()

    def _delete_ssh(self, user, ssh):
        url = self.url + '/users/%s/ssh/%s' % (user['id'], ssh['id'])
        request = requests.delete(url)
        self.assertEqual(200, request.status_code)

    def post(self, url, data=None):
        request = requests.post(url, json=data)
        self.addCleanup(rquests.delete, '%s/%s' % (url, request['id']))
