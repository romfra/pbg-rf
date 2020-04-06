# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 16:14:52 2020

@author: Romina
"""

# retrieve covid data from the European Centre for Disease Prevention and Control
# Code has been added in the github project: https://github.com/romfra/pbg-rf/

from bs4 import BeautifulSoup

import requests

# function to retrieve data from the site address
def getresponse(site):
    headers = {
        'authority': 'www.ecdc.europa.eu',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'sec-fetch-dest': 'document',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'accept-language': 'en,it;q=0.9,en-US;q=0.8',
        'cookie': 'cookieConsent=accepted; _ga=GA1.3.70351311.1585488794; _gid=GA1.3.1618863599.1585488794',
        'if-none-match': '^\\^1585489208-gzip^\\^',
        'if-modified-since': 'Sun, 29 Mar 2020 13:40:08 GMT',
    }
    
    return requests.get(site, headers=headers)

# function to parse the output from the get method
def parse_html(response):
    return BeautifulSoup(response.content, features="html.parser")

# function to find within the page a speicific tag
def getdata(tag,html):
    paragraphs = html.find_all(tag)
    #print(paragraphs)

    data = []

    for par in paragraphs:
        #for each tag the content is extracted (see exmaple)
        #<p> <strong> This is the part I want to extract </strong> </p>
        #becames <strong> This is the part I want to extract </strong>
        for p in par.contents:
            # list with countries and data are positioned after a bold paragaph
            # I isolate them splitting each paragraph using the tag the that closes the bold 
            value = str(p).replace('\xa0', '').split('</strong>')
            data.append(value)

    return data

def savetotaldeaths(data, sentence_start):
    
    # find the position of the title positioned before the data I'm looking for
    position = data.index(sentence_start)
    
    deaths = data[position + 1]
    # each combination of country - data is separated by comma
    deaths_by_country = [country for line in deaths for country in line.split(',')]
    
    i = 0
    csv_file = open('ecdc_covid_deaths.csv', 'w')
    csv_file.write('country,deaths_cases\n')
    while i < len(deaths_by_country):
        # the num deaths for each country is bracket
        index = deaths_by_country[i].find("(")
        # extract the country using the position of the bracket i.e. Italy (4444)
        country = deaths_by_country[i][1:index-1]
        #print(country)
        deaths_num = deaths_by_country[i][index+1:-1]
        #print(deaths_num)
        csv_file.write('"{0},{1}"\n'.format(country,deaths_num))
        i += 1
    csv_file.close()
    
def savecasesbycontinent(data, sentence_start):
    # find the position of the title positioned before the data I'm looking for
    position = data.index(sentence_start)
    
    start = position + 2
    continent = ''

    while continent != 'Other':
        # name of each continent is in bold
        #in the element we have '<strong>Europe'; to extarct the name of the continent
        # we have to extract from the 8th char
        continent = data[start][0][8:]
        cases = data[start+1]
        # each combination of country - data is separated by comma
        cases_by_country = [country for line in cases for country in line.split(',')]
        start +=2
        
        j = 0
        csv_file = open('ecdc_covid_cases_'+continent+'.csv', 'w')
        csv_file.write('country,cases\n')
    
        while j < len(cases_by_country):
            # extract the country using the position of the bracket ( i.e. Italy (4444)
            index = cases_by_country[j].find("(")
            if cases_by_country[j][1:2] == " ":
                # get rid of empty space at the beginning of the country name
                # get rid of * in some country name
                country = cases_by_country[j][2:index-1].replace('*','')
            else:
                country = cases_by_country[j][1:index-1].replace('*','')
            cases_num = cases_by_country[j][index+1:-1]
            csv_file.write('"{0},{1}"\n'.format(country,cases_num))
            j += 1
        csv_file.close()
        

def main():
    response = getresponse('https://www.ecdc.europa.eu/en/geographical-distribution-2019-ncov-cases')    
    
    soup = parse_html(response)
    
    rawdata = getdata('p',soup)
    
    savetotaldeaths(rawdata,['<strong>The deaths have been reported from', ''])
    
    savecasesbycontinent(rawdata,['<strong>Cases have been reported on the following continents:', ''])

if __name__ == '__main__':
    main()
