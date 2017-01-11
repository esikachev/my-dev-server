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

    def test_create_delete_user(self):
        url = 'http://localhost:5000/users'
        data = {
            "username": 'test_user1',
            "email": "em@em.com1",
            "password": 'pass1'
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
            'test_user',
            'mail@g.ru',
            'pass'
        ).json()
        url = 'http://localhost:5000/users/%s' % user['id']
        get_user = requests.get(url)

        self.assertEqual(200, get_user.status_code)
        self.assertEqual(user, get_user.json())

    def test_negative_create_exist_user(self):
        self._create_user(
            'test_user',
            'mail@g.ru',
            'pass'
        )
        self._create_user(
            'test_user',
            'mail@g.ru',
            'pass',
            expected_code=400
        )

    def test_create_delete_ssh(self):
        user = self._create_user(
            'test_user',
            'mail@g.ru',
            'pass'
        ).json()
        data = {
            "user_id": user.json['id'],
            "alias": 'testa',
            "host": '10.10.0.1',
            "username": 'testu',
            "password": "testp"
        }
        url = 'http://localhost:5000/users/%s/ssh' % user.json['id']
        new_ssh = requests.post(url, json=data)

        self.assertEqual(200, new_ssh.status_code)
        new_ssh = new_ssh.json()
        self.assertEqual(data['user_id'], new_ssh['user_id'])
        self.assertEqual(data['alias'], new_ssh['alias'])
        self.assertEqual(data['host'], new_ssh['host'])
        self.assertEqual(data['username'], new_ssh['username'])
        self.assertEqual(data['password'], new_ssh['password'])

        url = 'http://localhost:5000/users/%s/ssh/%s' % (
            user['id'],
            new_ssh['id']
        )
        request = requests.delete(url)
        self.assertEqual(200, request.status_code)
