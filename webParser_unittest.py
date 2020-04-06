# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 19:36:12 2020

@author: Romina
"""

import unittest
import os.path
from os import path
from webParser import getresponse, parse_html, getdata
class TestEcdcParse(unittest.TestCase): 
     
    # test if the website is reachable and there is not a 404 error page
    def testresponse(self):
        self.assertNotEqual(404, getresponse('https://www.ecdc.europa.eu/en/geographical-distribution-2019-ncov-cases').status_code)

    # testif the number of paragraph is as expected on the website
    def testFindAllByAttribute(self):
        matching = getdata('p',parse_html(getresponse('https://www.ecdc.europa.eu/en/geographical-distribution-2019-ncov-cases')))
        self.assertGreater(len(matching), 30)

    # test if the file with deaths data has been created
    # test if the file with deaths data has more than row (excluding the header)        
    def testfiledeaths(self):
        file_deaths = 'ecdc_covid_deaths.csv'
        deaths_data = [lines.strip() for lines in open(file_deaths, 'r')]
        self.assertTrue(path.exists(file_deaths))
        self.assertGreater(len(deaths_data),1)
        
    #test if the files with new cases data for each continent have been created
    # test if each file with deaths data has more than one row (excluding header)
    def testfilecases(self):
        continents = ['Africa','America','Asia','Europe','Oceania','Other']
        i = 0
        while i < len(continents):
            file_cases = 'ecdc_covid_cases_' + continents[i] + '.csv'
            cases_data = [lines.strip() for lines in open(file_cases, 'r')]
            self.assertTrue(path.exists(file_cases))
            self.assertGreater(len(cases_data),1)
            i += 1                              
        
if __name__ == '__main__':
    unittest.main()