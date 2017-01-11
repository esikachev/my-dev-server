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
        usr = requests.post(url, json=data)
        self.assertEqual(expected_code, usr.status_code)
        return usr.json()

    def test_create_delete_user(self):
        url = 'http://localhost:5000/users'
        data = {
            "username": 'test_user1',
            "email": "em@em.com1",
            "password": 'pass1'
        }
        user = requests.post(url, json=data)
        self.assertEqual(200, user.status_code)
        request = requests.delete(user['id'])
        self.assertEqual(200, request.status_code)

    def test_get_user(self):
        user = self._create_user(
            'test_user',
            'mail@g.ru',
            'pass'
        )
        url = 'http://localhost:5000/users/%s' % user['id']
        get_user = requests.get(url)

        self.assertEqual(200, requests.status_code)
        self.assertEqual(user, get_user.json())
