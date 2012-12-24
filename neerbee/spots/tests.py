from mongotesting import MongoTestCase
from neerbee.spots.models import Spot

class SpotTestCase(MongoTestCase):
    def setUp(self):
        # start by creating a new Spot object with its "name" set
        self.spot = Spot()
        self.spot.name = "The Diner"
        self.spot.address = "25 Curtain Rd."
        self.spot.neighbourhood = "Shoreditch"
        # save it to the database
        self.spot.save()
        
class SpotModelTest(SpotTestCase):
    def test_spot_created(self):
        # now check we can find in in the database again
        all_spots_in_database = Spot.objects.all()
        self.assertEquals(len(all_spots_in_database), 1)
        
    def test_spot_retrieved(self):
        all_spots_in_database = Spot.objects.all()
        only_spot_in_database = all_spots_in_database[0]
        self.assertEquals(only_spot_in_database, self.spot)
        
    # and check that it has saved its three attributes: name, address and neighbourhood
    def test_basic_info(self):
        all_spots_in_database = Spot.objects.all()
        only_spot_in_database = all_spots_in_database[0]   
        self.assertEquals(only_spot_in_database.name, self.spot.name)
        self.assertEquals(only_spot_in_database.address, self.spot.address)
        self.assertEquals(only_spot_in_database.neighbourhood, self.spot.neighbourhood)
