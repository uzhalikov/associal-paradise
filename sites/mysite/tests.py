from django.test import TestCase
from mysite.models import Car

class CarTestCase(TestCase):
    def setUp(self):
        Car.objects.create(model="Porshe 911", engine="2,8L", maxspeed=250)
        Car.objects.create(model="Porshe Boxster", engine="4,0L", maxspeed=300)
        Car.objects.create(model="Porshe Boxster2",
                           engine=4.0, maxspeed=300)

    def testCar(self):
        car = Car.objects.get(model="Porshe 911")
        car2 = Car.objects.get(model="Porshe Boxster")
        car3 = Car.objects.get(model="Porshe Boxster2")
        self.assertEqual(
            car.maxSpeed(), 'Max speed "Porshe 911" is 250. The engine is 2,8L')
        self.assertEqual(
            car2.maxSpeed(), 'Max speed "Porshe Boxster" is 300. The engine is 4,0L')
        self.assertEqual(
            car3.maxSpeed(), 'Max speed "Porshe Boxster2" is 300. The engine is 4,0L')


