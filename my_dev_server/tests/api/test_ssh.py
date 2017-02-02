import requests

from my_dev_server.tests.api import base
from my_dev_server import utils


class TestSsh(base.Base):

    def test_create_delete_ssh(self):
        """Scenario:
          - create user
          - create new ssh
          - check that ssh was created correctly
          - delete ssh
          - delete user
        """
        user = self.create_user()

        ssh = self.create_ssh(user['id'])

        self.check_response(data, ssh)

        self.delete_user(user['id'], ssh['id'])

    def test_get_ssh(self):
        """Scenario:
          - create user
          - create new ssh
          - get ssh by id
          - get ssh by host
          - check that ssh is correct
          - delete ssh
          - delete user
        """
        user = self.create_user()
        
        ssh = self.create_ssh(user['id'])
        
        get_ssh_by_id = self.get_ssh(user['id'], ssh['id'])
        self.check_response(ssh, get_ssh_by_id)

        get_ssh_by_host = self.get_ssh(user['id'], ssh['host'])
        self.check_response(ssh, get_ssh_by_host)

        self.delete_ssh(user, ssh)
        self.delete_user(user)

    def test_create_exist_ssh(self):
        """Scenario:
          - create user
          - create ssh
          - try to create ssh with same data
          - check that 2'nd ssh was not created
          - delete ssh
          - delete user
        """
        user = self.create_user()

        data = self.create_ssh(user['id'])
        
        ssh.update({'expected_code': 409})
        exist_ssh = self.create_ssh(**ssh)

        self.delete_ssh(user, new_ssh.json())
        self.delete_user(user)

    def check_response(self, data, ssh):
        self.assertEqual(data['user_id'], ssh['user_id'])
        self.assertEqual(data['alias'], ssh['alias'])
        self.assertEqual(data['host'], ssh['host'])
        self.assertEqual(data['ssh_username'], ssh['ssh_username'])
        self.assertEqual(data['ssh_password'], ssh['ssh_password'])

