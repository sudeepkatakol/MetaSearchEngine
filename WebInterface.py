'''
Google Custom Search API usage.
Author: Caio Granero
Check this out: https://github.com/caiogranero/google-custom-search-api-python
'''

# __author__ = 'Caio Granero'

from urllib2 import urlopen
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import json
import re
import requests
import os
from bs4 import Comment
from Scraper import extract_content_with_Arc90 

class SearchResult:
    def __init__(self, title, link, snippet):
        '''
        distribution contains the probability distribution (in %) for a particular SearchResult
        top3 has the name of the class and the corresponding probability for the top 3 probabilities. 
        '''
        self.title = title
        self.link = link
        self.snippet = snippet
        self.distribution = None
        self.top3 = None

    def calc_top3(self):
        '''
        Sorts the arguments of the probability distribution wrt to the probability
        Then adds the name of the class and the corresponding probability to a tuple 
        '''
        classes = ['Animals', 'Authors_Poets', 'English_Literature', 'Geography', 'History', 'Mathematics', 'Science', 'Sociology_Economics_Politics']
        arr = self.distribution.argsort()[-3:][::-1]
        self.top3 = ({classes[arr[0]]: self.distribution[arr[0]]}, {classes[arr[1]]: self.distribution[arr[1]]},
                     {classes[arr[2]]: self.distribution[arr[2]]})

SEARCH_ENGINE_ID = '003580089669486167640:co2f0smzoku'

# The key here is Caio Granero's developerKey, use your own.
def _get_service():
    '''
    Helper function. See Caio Granero's code. Link at the top this page    
    '''
    service = build("customsearch", "v1",
                    developerKey="AIzaSyDxpJfGwM9KzeTFlKa-_Z-wEgI1sKMcKKo")

    return service


def _main(search_query, page_limit, filename):
    '''
    Helper function. See Caio Granero's code. Link at the top this page    
    The results are dumped in the json file specified.
    '''
    service = _get_service()
    startIndex = 1
    response = []

    for nPage in range(0, page_limit):
        # print "Reading page number:",nPage+1

        response.append(service.cse().list(
            q=search_query,  # Search words
            cx=SEARCH_ENGINE_ID,  # CSE Key
            lr='lang_en',  # Search language
            start=startIndex
        ).execute())

        startIndex = response[nPage].get("queries").get("nextPage")[0].get("startIndex")

    with open(filename, 'w') as outfile:
        json.dump(response, outfile)


def get_search_results(search_query, page_limit=1):
    '''
    Extarcts the title, link and the snippet from each result obtained (contained in the JSON file)
    For JSON file structure refer to Caio Granero's github page mentioned above 
    '''
    _main(search_query, page_limit, 'data1.json')
    search_results = []
    with open('data1.json') as json_data:
        d = json.load(json_data)
    for i in range(len(d)):
        for j in range(len(d[i]['items'])):
            search_results.append(SearchResult(d[i]['items'][j]['title'], d[i]['items'][j]['link'], d[i]['items'][j]['snippet']))
    os.remove('data1.json')
    return search_results

'''
# returns a string
def scrape(url):
    html = urlopen(url, timeout=3).read().decode('utf-8')
    return BeautifulSoup(html, 'lxml').get_text()
'''


'''
Set the timeout in accordance to the slowness of your internet connection.
Better scraping utility can help improve the performance of the algorithm
'''
def scrape(url):
    '''
    Scrapes with the help of Arc90 function (see the Scraper module)
    '''
    html_string = requests.get(url, timeout=4).text
    return extract_content_with_Arc90(html_string)
    