# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 15:57:34 2020

@author: Romina
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 19:36:12 2020

@author: Romina
"""

import unittest
import os.path
from os import path
from Rental_car import Dealership
class TestDealership(unittest.TestCase):

    def setUp(self):
        self.dealership = Dealership()
        self.dealership.create_current_stock('D',6)
        self.dealership.create_current_stock('E',10)
        self.dealership.create_current_stock('P',12)
        self.dealership.create_current_stock('H',4)
        
        
       
        
    def testCreateStock(self):
        self.assertEqual(6, len(self.dealership.diesel_cars))
        self.assertEqual(10, len(self.dealership.electric_cars))
        self.assertEqual(12, len(self.dealership.petrol_cars))
        self.assertEqual(4, len(self.dealership.hybrid_cars))
        
        
    def testRentCar(self):
        # rent stock 10 P cars
        self.dealership.rentCar(self.dealership.petrol_cars, 10, 'P', '')
        self.assertEqual(2, len(self.dealership.petrol_cars))
        
        # rent stock 5 E cars 
        self.dealership.rentCar(self.dealership.electric_cars, 5, 'E', '')
        self.assertEqual(5, len(self.dealership.electric_cars))
        
        #rent stock 6 D cars
        self.dealership.rentCar(self.dealership.diesel_cars, 6, 'D', '')
        self.assertEqual(0, len(self.dealership.diesel_cars))
        
       
    def testReturnCar(self):
        # return 5 petrol cars
        self.dealership.returnCar(self.dealership.petrol_cars,5)
        self.assertEqual(17, len(self.dealership.petrol_cars))
        
        #return 1 electric car
        self.dealership.returnCar(self.dealership.electric_cars,1)
        self.assertEqual(11, len(self.dealership.electric_cars))
        
        #return 3 diesel cars
        self.dealership.returnCar(self.dealership.diesel_cars,3)
        self.assertEqual(9, len(self.dealership.diesel_cars))
        
        #return 4 hybrid cars
        self.dealership.returnCar(self.dealership.hybrid_cars,4)
        self.assertEqual(8, len(self.dealership.hybrid_cars))
        
    def testfileoutput(self):
        self.dealership.save_csv()
        file = 'cars.csv'
        cars = [lines.strip() for lines in open(file, 'r')]
        self.assertTrue(path.exists(file))
        self.assertGreater(len(cars),1)
        self.assertEqual(12, int(cars[1][2:]))
        self.assertEqual(10, int(cars[2][2:]))
        self.assertEqual(6, int(cars[3][2:]))
        self.assertEqual(4, int(cars[4][2:]))
        

if __name__ == '__main__':
    unittest.main()