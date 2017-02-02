import requests
import testtools

from my_dev_server import utils


class Base(testtools.TestCase):

    def setUp(self):
        super(Base, self).setUp()
        url = 'http://localhost:5000'
        self.users_base_url = url + '/users'
        self.users_url = self.users_base_url + '/%s'
        self.ssh_base_url = url + '/users/%s/ssh'
        self.ssh_url = self.ssh_base_url + '/%s'

    def create_user(self, username=utils.rand_name('username'),
                    password=utils.rand_name('password'),
                    email=utils.rand_name('email'), expected_code=200,
                    error_msg=None):
        data = {
            "username": username,
            "password": password,
            "email": email
        }
        user = requests.post(self.users_base_url, json=data)
        self.assertEqual(expected_code, user.status_code)
        if error_msg:
            self.assertEqual(error_msg, user.message)
        return user.json()

    def get_user(self, user_id, expected_code=200):
        url = self.users_url % user_id
        get_user = requests.get(url)
        self.assertEqual(expected_code, get_user.status_code)
        return get_user.json()

    def delete_user(self, user_id, expected_code=200):
        url = self.users_url % user_id
        request = requests.delete(url)
        self.assertEqual(expected_code, request.status_code)

    def create_ssh(self, user_id, alias=utils.rand_name('alias'),
                   host=utils.rand_name('host'),
                   username=utils.rand_name('username'),
                   password=utils.rand_name('password'),
                   expected_code=200):
        data = {
            "user_id": user_id,
            "alias": alias,
            "host": host,
            "ssh_username": username,
            "ssh_password": password
        }
        url = self.ssh_base_url % user_id
        new_ssh = requests.post(url, json=data)
        self.assertEqual(expected_code, request.status_code)
        return new_ssh.json()
    
    def get_ssh(self, user_id, ssh_id, expected_code=200):
        url = self.ssh_url % (user_id, ssh_id)
        request = requests.get(url)
        self.assertEqual(expected_code, request.status_code)
        return request.json()


    def delete_ssh(self, user_id, ssh_id, expected_code=200):
        url = self.ssh_url % (user_id, ssh_id)
        request = requests.delete(url)
        self.assertEqual(expected_code, request.status_code)
