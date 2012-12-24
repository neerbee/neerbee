from mongotesting import MongoTestCase
from neerbee.spots.models import Spot

class SpotModelTestCase(MongoTestCase):
    def setUp(self):
        # start by creating a new Spot object with its "name" set
        self.spot = Spot()
        spot.name = "The Diner"
        spot.address = "25 Curtain Rd."
        spot.neighbourhood = "Shoreditch"
        # save it to the database
        spot.save()
        
class SpotModelTest(SpotModelTestCase):
    def test_spot_created(self):
        # now check we can find in in the database again
        all_spots_in_database = Spot.objects.all()
        self.assertEquals(len(all_spots_in_database), 1)
        
    def test_spot_retrieved(self):
        only_spot_in_database = all_spots_in_database[0]
        self.assertEquals(only_spot_in_database, spot)
        
    # and check that it has saved its three attributes: name, address and neighbourhood
    def test_name(self):   
        self.assertEquals(only_spot_in_database.name, spot.name)
        
    def test_address(self):
        self.assertEquals(only_spot_in_database.address, spot.address)
        
    def test_neighbourhood(self):
        self.assertEquals(only_spot_in_database.neighbourhood, spot.neighbourhood)
