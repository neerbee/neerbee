from mongotesting import MongoTestCase
from django.core.urlresolvers import reverse
from neerbee.spots.models import *

class SpotTestCase(MongoTestCase):
    def setUp(self):
        # start by creating a new Spot object with its "name" set
        self.spot = Spot()
        self.spot.name = "The Diner"
        self.spot.address = "25 Curtain Rd."
        self.spot.neighbourhood = "Shoreditch"
        food_service = ServiceFood()
        food_service.category = "Diner"
        food_service.delivery = False
        food_service.take_out = True
        bar_service = ServiceBar()
        bar_service.category = "Bar"
        self.spot.services = [food_service, bar_service]
        self.spot.price = 2
        # save it to the database
        self.spot.save()
        
class SpotModelTest(SpotTestCase):
    def test_spot_created(self):
        # now check we can find it in the database again
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
     
    def test_services(self):
        all_spots_in_database = Spot.objects.all()
        only_spot_in_database = all_spots_in_database[0]
        self.assertEquals(only_spot_in_database.services[0].category, "Diner")   

class SpotFormTest(SpotTestCase):
    # test the validation of the view that creates a new spot
    def test_new_spot_view_validation(self):
        # log user in
        resp = self.client.login(username='nikos', password='123')
        self.assertTrue(resp)

        # send no POST data
        resp = self.client.post(reverse('admin:create_spot'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('form' in resp.context)
        self.assertTrue('spot_slug' in resp.context)
        self.assertEqual(resp.context['form']['name'].errors,
                            [u'This field is required.'])
        self.assertEqual(resp.context['form']['address'].errors,
                            [u'This field is required.'])
        self.assertEqual(resp.context['form']['neighbourhood'].errors,
                            [u'This field is required.'])
        self.assertEqual(resp.context['form']['pobox'].errors,
                            [u'This field is required.'])
        self.assertEqual([u'Spot must offer at least one service.'],
                        resp.context['form'].non_field_errors())

        # must specify food category
        resp = self.client.post(reverse('admin:create_spot'), 
                                {'service_food': True})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([u'Must specify food category.'],
                        resp.context['form'].non_field_errors())
                  
        # must specify bar category
        resp = self.client.post(reverse('admin:create_spot'), 
                                {'service_bar': True})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([u'Must specify bar category.'],
                        resp.context['form'].non_field_errors())
    
    # test that the view inserts new spot correctly    
    def test_create_spot_view(self):
        # log user in
        resp = self.client.login(username='nikos', password='123')
        self.assertTrue(resp)

        # send valid POST data
        resp = self.client.post(reverse('admin:create_spot'),
                                {'name': 'Busaba',
                                 'address': '1-6 Batemans Row',
                                 'neighbourhood': 'Shoreditch',
                                 'pobox': 'EC2A3HH',
                                 'service_food': True,
                                 'food_category': 'Thai'})
        # should be redirected to /spots/
        self.assertEqual(resp.status_code, 302)
        # get the saved spot
        bus = Spot.objects(name='Busaba')
        bus = bus[0]
        self.assertIsNotNone(bus)
        # and check that data was saved correctly
        self.assertEqual(bus.name, 'Busaba')
        self.assertEqual(bus.address, '1-6 Batemans Row')
        self.assertEqual(bus.neighbourhood, 'Shoreditch')
        self.assertEqual(bus.pobox, 'EC2A3HH')
        self.assertIsInstance(bus.services[0], ServiceFood)
        self.assertEqual(bus.services[0].category, 'Thai')

    # then test the view that edits an existing spot
    def test_edit_spot_view(self):
        # log user in
        resp = self.client.login(username='nikos', password='123')
        self.assertTrue(resp)
        # post for existing slug changing the address
        resp = self.client.post(reverse('admin:create_spot'),
                                {'spot_slug': 'busaba',
                                 'name': 'Busaba',
                                 'address': 'P Benaki',
                                 'neighbourhood': 'Soho',
                                 'pobox': 'EC2A3HH',
                                 'service_food': True,
                                 'food_category': 'Thai'})
        # should be redirected to /spots/
        self.assertEqual(resp.status_code, 302)
        # get the saved spot
        bus = Spot.objects(name='Busaba')
        # check that the spot was edited and not a new one created
        self.assertEqual(len(bus), 1)
        bus = bus[0]
        self.assertIsNotNone(bus)
        # and check that data was saved correctly
        self.assertEqual(bus.address, 'P Benaki')
        self.assertEqual(bus.neighbourhood, 'Soho')