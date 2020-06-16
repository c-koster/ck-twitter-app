"""
Culton Koster - 8/12
urllib media crawler
Uses urllib and SQLite3 to crawl a list of news site and store word-usage
 statistics for analysis purposes. Also notes when a person of interest
 is mentioned in an article.

Notes:

"""
import sys
import urllib.request, urllib.parse, urllib.error, urllib.robotparser
from bs4 import BeautifulSoup, SoupStrainer
import re
import copy


SEARCH_STRING = 'href="https'
keywords = []

class Output:

    def __init__(self,text):
        self.text = text


def crawl(start_urls,scope=5):
    """
    Function which navigates html code, and performs breadth-first search on
    the supplied url(s). Scope will count downward to 0, so note that this will crawl
    """
    output = []
    to_do = start_urls
    vis = [] # tracks visited sites
    while (scope>0):
        url = to_do[0]
        print('\nscope: ' + str(scope) + '\n'+ ('-'*10))
        print("scanned: " + url)
        if can_crawl(url) and (url not in vis):
            vis.append(url) # mark it as visited
            scraped_urls,out = scan_page(url) # grab the urls from the page.
        to_do.remove(url)
        to_do += scraped_urls # add all uls found in the page
        if out != None:
            output.append(out)
        scope -=1

    return vis,output

def scan_page(url):
    """
    Takes in a single address as a parameter, and outputs all the ones it finds.
    Also calls an analyze_page function to do other aforementioned operations.
    """
    urls = []
    with urllib.request.urlopen(url) as webpage:
        for link in BeautifulSoup(webpage, parse_only=SoupStrainer('a'),features="html.parser"):
            if link.has_attr('href'):
                urls.append(link['href'])
    o = Output(analyze_page(urllib.request.urlopen(url))) # TODO fix this. big mess

    for link in urls:
        if ("https://" not in link):
            urls.remove(link)

    return urls,o


def can_crawl(url):
    """
    Reads the robots.txt file to avoid breaking any laws !!
    """
    try:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(str(url) + '/robots.txt') # need to parse this part to end in .com
        rp.read()
        return rp.can_fetch("*",url)
    except error.URLError as e:
        return False

def analyze_page(content):
    """
    extracts and collects text content from the page.
    """
    soup = BeautifulSoup(content,'html.parser')
    text = soup.find_all(text=True)
    output = ''
    blacklist = ['[document]','noscript','header','html','meta','head', 'input','script','style']
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    return output

def run():
    scope = 100
    sitelist = ["https://www.wsj.com"]
    links,outputlist = crawl(sitelist,scope)

    for i in outputlist:
        s = i.text.replace('\n','.').split('.')
        if 'Koster' in i:
            print(i)
            print('\n')

    print('scanned ' + str(len(outputlist)) + ' sites with scope = ' +str(scope))


if __name__ == '__main__':
    run()
