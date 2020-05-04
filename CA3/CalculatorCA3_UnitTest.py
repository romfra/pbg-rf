# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 19:36:12 2020

@author: Romina
"""

import unittest
from Calculator_CA3 import Calculator
class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = Calculator()
       
        
    def testAddition(self):
        # test addition between lists
        self.assertEqual([27,16,12], self.calculator.add([15,8,5],[12,8,7])) 
        self.assertEqual([12,5], self.calculator.add([11,3,5],[1,2]))
        
        
    def testGeneratorAddition(self): 
        # test running total with generator
        running_add = self.calculator.gen_sum([10,20,30])
    
        self.assertEqual(10, next(running_add))
        self.assertEqual(30, next(running_add))
        self.assertEqual(60, next(running_add))
        
    def testSubtract(self):
        # test subtraction between lists
        self.assertEqual([-10,2,7], self.calculator.subtract([20,8,15], [30,6,8]))
        self.assertEqual([0,-3,18], self.calculator.subtract([5,12,15], [5,15,-3,2]))
        # test running subtraction 
        self.assertEqual(10, self.calculator.subtract([25,5,10],''))
        
    def testDivision(self):
        # test division between lists's values
        self.assertEqual([1.5,10,-8], self.calculator.divide([3,40,8],[2,4,-1]))
        #test division with an element = 0 as denominator
        self.assertEqual([3,5], self.calculator.divide([9,40,8],[3,8,0]))
        
    def testMultiply(self):
        # test multiplication between list's values
        self.assertEqual([12,100,-8], self.calculator.multiply([3,10,8],[4,10,-1]))
        self.assertEqual([55,20], self.calculator.multiply([5,4],[11,5,6,5]))
        
    def testSquareRootFilter(self):
        # test that the negative numbers are filtered out
         square_roots = self.calculator.square_root([25,169,-100])
         self.assertEqual(2, sum(1 for n in square_roots))
         
    
    def testSquareRoot(self):
        square_roots = self.calculator.square_root([25,169,-100])       
        #test the calculation of square root
        self.assertEqual(5, next(square_roots))
        self.assertEqual(13, next(square_roots))
        
    def testPower(self):
        # test the power calculation
        self.assertEqual([8,36,256,25], self.calculator.power([2,6, 4, -5],[3,2,4,2,8]))
    
    
    def testLog(self):
        #test the filter for negative numbers not allowed in the ln function
        self.assertEqual(3, len(self.calculator.log([50,20,20,-90],'','1')))
        self.assertEqual([2.30,3.22,4.22] , self.calculator.log([10,25,68],'', '1'))
        
        #test the filter for negative numbers not allowed in the log function
        self.assertEqual(3, len(self.calculator.log([50,20,20,-90],[10,10,10],'2')))
        self.assertEqual([1.7,1.3,1.48], self.calculator.log([50,20,30],[10,10,10],'2'))
        
    def testSin(self):
        self.assertEqual([0, 0.5, 1], [round(num,2) for num in self.calculator.sen([180, 30, 90])])   
        
    def testCosin(self):
        self.assertEqual([-1,0.87, 0], [round(num,2) for num in self.calculator.cos([180, 30, 90])]) 
        
    def testTan(self):
        tangents = self.calculator.tan([180,30,120])       
        #test the calculation of square root
        self.assertEqual(-0.0, round(next(tangents),3))
        self.assertEqual(0.577, round(next(tangents),3))
        self.assertEqual(-1.732, round(next(tangents),3))

if __name__ == '__main__':
    unittest.main()