from mongotesting import MongoTestCase
from neerbee.spots.models import Spot

class SpotModelTest(MongoTestCase):
    def test_creating_a_new_spot(self):
        # start by creating a new Spot object with its "name" set
        spot = Spot()
        spot.name = "The Diner"
        spot.address = "25 Curtain Rd."
        spot.neighbourhood = "Shoreditch"

        # check we can save it to the database
        spot.save()

        # now check we can find in in the database again
        all_spots_in_database = Spot.objects.all()
        self.assertEquals(len(all_spots_in_database), 1)
        only_spot_in_database = all_spots_in_database[0]
        self.assertEquals(only_spot_in_database, spot)

        # and check that it has saved its three attributes: name, address and neighbourhood
        self.assertEquals(only_spot_in_database.name, spot.name)
        self.assertEquals(only_spot_in_database.address, spot.address)
        self.assertEquals(only_spot_in_database.neighbourhood, spot.neighbourhood)
