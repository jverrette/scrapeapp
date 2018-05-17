import math
import urllib3
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re

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
    return 'default'

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
    return pd.Series(lister)

def emails(lister):
    for idx, phrase in enumerate(lister):
        try:
            match = re.search('(<)?(\w+@\w+(?:\.\w+)+)(?(1)>)', lister[idx])
            return match.group(0)
        except:
            pass
    return ''


def hatePandas(x):
    if isinstance(x, (list, tuple)):
        if x==[]:
            return None
        else:
            return x[0]
    else:
        return x
# This cleaning function initially cleans the data and puts all of the month words in the same form
def clean(df):
    df = df.str.lower()
    df = df.str.strip()
    mask = df.str.contains(r'\b\d{1,2}-\d{1,2}-\d{2,4}\b')
    df[mask] = df[mask].str.replace('-','/')
    df[~mask] = df[~mask].str.replace('-',' ')
    df = df.str.replace('[,.]','')
    df = df.str.replace(r'(\d+(th|nd|st)\b)','')
    # alter df to only include month abbreviations
    df = df.str.replace(r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\b',
                   lambda x: x.groups()[0][:3])
    # alter df to always include day of week
    df = df.str.replace(r'\b\d{1,2}/\d{4}$', lambda m: '/01/'.join(m.group().split('/'))) 
    return df

def createDF(df):
    # Create initial month, day, and year columns
    output = pd.DataFrame(index=df.index, columns=['dates', 'month','day','year','output'])
    # Find mask of where number dates are in df
    numbers = df.str.contains(r'(?:\b\d{1,2}/)?\d{1,2}/\d{2,4}\b')
    if any(numbers):
    # assign columns values for the number dates
        output['dates'].loc[numbers] = df[numbers].str.findall(r'(?:\d{1,2}/)?\d{1,2}/\d{2,4}')
        output['dates'].loc[numbers] = df[numbers].str.findall(r'(?:\b\d{1,2}/)?\d{1,2}/\d{2,4}\b|\b20\d{2}\b')
        output['dates'].loc[numbers] = output['dates'].loc[numbers].apply(lambda x: x[0].strip())
        output['month'].loc[numbers] = output['dates'].loc[numbers].str.findall(r'(\b\d{1,2})(?:/\d{1,2})?/\d{2,4}\b')
    # month numbers
        output['year'].loc[numbers] = output['dates'].loc[numbers].str.findall(r'(?:\d{1,2}/)?\d{1,2}/(\d{2,4})\b')
    # year numbers
        output['day'].loc[numbers] = output['dates'].loc[numbers].str.findall(r'\b\d{1,2}/(\d{1,2})/\d{2,4}\b')
    # day numbers
                
    #numbers = df.str.contains(r'(?:\b\d{1,2}/)?\d{1,2}/\d{2,4}\b|((?:\d{1,2} )?(?:[a-z]{3} )?(?:\d{1,2} )?\d{4})|\b20\d{2}\b')

    
    # assign columns values for the word dates
    # isolate all dates from words
    output['dates'].loc[~numbers] = df[~numbers].str.findall(r'((?:\d{1,2} )?(?:[a-z]{3} )?(?:\d{1,2} )?\d{4})')
    #DF['dates'].iloc[~numbers] = DF['dates'].apply(lambda x:x[0])
    output['dates'].loc[~numbers] = output['dates'].loc[~numbers].apply(lambda x: hatePandas(x))
    # create dictionary to get the number value from the months
    dictionary = {'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}
    output['month'].loc[~numbers] = output['dates'].loc[~numbers].str.findall(r'\b([a-z]{3})\b') # month words
    output['month'] = output['month'].apply(
        lambda x: hatePandas(x))
    output['month'].loc[~numbers] = output['month'].loc[~numbers].apply(
        lambda x: str(dictionary[x]) if (x in dictionary) else '01') # If no value in month, choose 01
    output['year'].loc[~numbers] = output['dates'].loc[~numbers].str.findall(r'(\d{4})') # year words
    output['year'] = output['year'].apply(lambda x: hatePandas(x))
    output['day'].loc[~numbers] = output['dates'].loc[~numbers].str.findall(r'(\b\d{1,2}\b)') # day words
    output['day'] = output['day'].apply(lambda x: hatePandas(x))

    # Get rid of any unnecessary columns
    output = output[~output['dates'].isnull()]

# For all of the rows in output
    output['year'] = output['year'].apply(lambda x: '20'+x if  (x is not None)&(len(x)==2) else x)
# If value in month or day has length 1, choose to add a 0 on the left
    for column in ['month', 'day']:
        output[column] = output[column].apply(lambda x: x if x!=None else '01')
        output[column] = output[column].apply(lambda x: x if len(x)>0 else '01')
        output[column] = output[column].apply(lambda x: x if len(x)>1 else '0'+x)
    output['output'] = output.apply(lambda row: '/'.join([row['month'],row['day'],row['year']]), axis=1)
    return output

# Returns only the most recent date available
def date_sorter(stringer):
    DF = createDF(clean(db(stringer)))
    DF = DF.sort_values(by=['year', 'month', 'day'], ascending=False)
    return DF['output'].iloc[0]

#pythonFile.createDF(pythonFile.clean(pythonFile.db(stringer)))
# (<)?(\w+@\w+(?:\.\w+)+)(?(1)>)
