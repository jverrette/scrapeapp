import math
import urllib3
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def count(stringer):
    #specify the url
    stringer = stringer.replace(' ', '+')
    wiki = 'https://en.wikipedia.org/w/index.php?search='+stringer+'&title=Special:Search&go=Go&fulltext=1'

#Query the website and return the html to the variable 'page'
    http = urllib3.PoolManager()
    page = http.request('GET', wiki)

#Parse the html in the 'page' variable, and store it in Beautiful Soup format
    soup = BeautifulSoup(page.data, "lxml")

#print(soup.prettify())
    s = str(soup.findAll(attrs={"class" : "results-info"}))
    b = s[s.find('data-mw-num-results-total="')+27:]
    return b[:b.find('"')] #returns the number in a string

def sqrt(number):
    return 'Version '+ str(math.sqrt(number))

def date(stringer):
    wiki = 'http://petdoc.ch/'
    wiki = stringer
#Query the website and return the html to the variable 'page'
    http = urllib3.PoolManager()
    page = http.request('GET', wiki)

#Parse the html in the 'page' variable, and store it in Beautiful Soup format
    soup = BeautifulSoup(page.data, "lxml")
    hey = [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]

    contents = soup.find_all("p")
    outputText = [contents[i].get_text() for i in range(len(contents))]
    # split up the list further based on new lines or tabs
    # having various lines will make it easier to distinguish between important information and various words
    lister = []
    for i in range(len(outputText)):
        lister.extend(outputText[i].split("\n"))
    return soup.getText()
