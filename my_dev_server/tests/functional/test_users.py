import requests
import testtools


class TestUsers(testtools.TestCase):

    def _create_user(self, username, email, password,
                     expected_code=200):
        url = 'http://localhost:5000/users'
        data = {
            "username": username,
            "email": email,
            "password": password
        }
        user = requests.post(url, json=data)
        self.assertEqual(expected_code, user.status_code)
        return user

    def _delete_user(self, user):
        url = 'http://localhost:5000/users/%s' % user['id']
        request = requests.delete(url)
        self.assertEqual(200, request.status_code)


    def test_create_delete_user(self):
        url = 'http://localhost:5000/users'
        data = {
            "username": 'test_user1',
            "email": "user@mail1.com",
            "password": 'pass'
        }
        user = requests.post(url, json=data)
        self.assertEqual(200, user.status_code)
        user = user.json()
        self.assertEqual(data['username'], user['username'])
        self.assertEqual(data['email'], user['email'])
        self.assertEqual(data['password'], user['password'])
        url = 'http://localhost:5000/users/%s' % user['id']
        request = requests.delete(url)
        self.assertEqual(200, request.status_code)

    def test_get_user(self):
        user = self._create_user(
            'test_user2',
            'user@mail2.com',
            'pass'
        ).json()
        url = 'http://localhost:5000/users/%s' % user['id']
        get_user = requests.get(url)

        self.assertEqual(200, get_user.status_code)
        self.assertEqual(user, get_user.json())
        self._delete_user(user)


    def test_create_delete_ssh(self):
        user = self._create_user(
            'test_user3',
            'user@mail3.com',
            'pass'
        ).json()
        data = {
            "user_id": user['id'],
            "alias": 'test_alias',
            "host": '10.10.0.1',
            "username": 'test_username',
            "password": "testp_pass"
        }
        url = 'http://localhost:5000/users/%s/ssh' % user['id']
        new_ssh = requests.post(url, json=data)

        self.assertEqual(200, new_ssh.status_code)
        new_ssh = new_ssh.json()
        self.assertEqual(data['user_id'], new_ssh['user_id'])
        self.assertEqual(data['alias'], new_ssh['alias'])
        self.assertEqual(data['host'], new_ssh['host'])
        self.assertEqual(data['username'], new_ssh['username'])

        url = 'http://localhost:5000/users/%s/ssh/%s' % (
            user['id'],
            new_ssh['id']
        )
        request = requests.delete(url)
        self.assertEqual(200, request.status_code)
        self._delete_user(user)
