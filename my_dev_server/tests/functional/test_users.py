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
        usr = requests.post(url, data)
        assert expected_code == usr.status_code
        return usr.json()

    def test_create_delete_user(self):
        url = 'http://localhost:5000/users'
        data = {
            "username": 'test_user',
            "email": "em@em.com",
            "password": 'pass'
        }
        user = requests.post(url, data)
        assert user.status_code == 200
        request = requests.delete(user['id'])
        assert request.status_code == 200

    def test_get_user(self):
        user = self._create_user(
            'test_user',
            'mail@g.ru',
            'pass'
        )
        url = 'http://localhost:5000/users/%s' % user['id']
        get_user = requests.get(url)

        assert get_user.status_code == 200
        assert get_user.json() == user
