import math
import urllib3
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re

def db(stringer):
    #wiki = 'http://petdoc.ch/'
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
    return lister

def emails(lister):
    for idx, phrase in enumerate(lister):
        try:
            match = re.search('(<)?(\w+@\w+(?:\.\w+)+)(?(1)>)', lister[idx])
            return match.group(0)
        except:
            pass
    return 'None Available'

def phone(lister):
    usa = '(1|\+1)?([ -])?(\d{3}|\(\d{3}\))?([ -])?\d{3}([ -])?\d{4}'
    swiss = '(41|\+41)?(0|\(0\))?\d{2}([ -])?\d{3}([ -])?\d{2}([ -])?\d{2}'
    china = '(86|\+86)?([ -])?1\d{2}([ -])?\d{4}([ -])?\d{4}'
    for regrex in [usa, swiss, china]:
        for idx, phrase in enumerate(lister):
            try:
                match = re.search(regrex, lister[idx])
                return match.group(0)
            except:
                pass
    return 'None Available'
