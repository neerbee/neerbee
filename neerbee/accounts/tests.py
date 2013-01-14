from mongotesting import MongoTestCase
from neerbee.users.models import Bee


class AccountTestCase(MongoTestCase):
    def test_login(self):
    	#Bee.create_user(username="nikos", email="nikos@neerbee.com", password="123")
    	resp = self.client.login(username='nikos', password='123')
    	self.assertEqual(resp, True)
