from mongotesting import MongoTestCase
from neerbee.users.models import Bee


class AccountTestCase(MongoTestCase):
    def test_login(self):
    	# test that default user can be logged in
    	resp = self.client.login(username='nikos', password='123')
    	self.assertEqual(resp, True)
