import urllib3, sys, re
from bs4 import BeautifulSoup

def get_soup(wiki):
    urllib3.disable_warnings()
    http = urllib3.PoolManager()
    page = http.request('GET', wiki)
    # also break up by <br /> tags which refer to new lines
    # replace <br /> with a new line \n
    output = str(page.data).replace("<br/>", '\n')
    #Parse the html and convert to Beautiful Soup format
    return BeautifulSoup(output, "lxml")

def facebook(soup):
    links = soup.find_all('a') 
    for idx, link in enumerate(links):
        try:
            match = re.search('facebook', link.get('href'))
         
            if match.group(0):
                return link.get('href')
         
        except:
            pass
    return ''


def instagram(soup):
    links = soup.find_all('a') 
    for idx, link in enumerate(links):
        try:
            match = re.search('instagram', link.get('href'))
         
            if match.group(0):
                return link.get('href')
         
        except:
            pass
    return ''

def db(soup):

    hey = [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]

    contents = soup.find_all("p")
    outputText = [content.get_text() for content in contents]
    # split up the list further based on new lines or tabs
    # having various lines will make it easier to distinguish between important information and various words
    lister = []
    for phrase in outputText:
        lister.extend(phrase.split("\n"))
    return lister

def emailLink(soup):
    links = soup.find_all('a') 
    for link in links:
        try:
            match = re.search('mailto:', link.get('href'))
         
            if match.group(0):
                output = link.get('href')
                return output.replace("mailto:", "")
         
        except:
            pass
    return ''

def email(soup, lister):
    emailFromLink = emailLink(soup)
    if bool(emailFromLink):
        return emailFromLink
    for idx, phrase in enumerate(lister):
        try:
            match = re.search('(<)?(\w+@\w+(?:\.\w+)+)(?(1)>)', lister[idx])
            output = match.group(0)
            #print(phrase)
            return output
        except:
            pass
    return ''

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
    return ''

def contact(stringer, soup):
# stringer is the original websites
# soup is the beautiful soup variable resulting from the original website
# Returns either:
#1. the first link available on page with the word contact or kontact in the title
#2. ''
    links = soup.find_all('a') 
    for idx, link in enumerate(links):
        try:
            match = re.search('(contact)|(kontakt)|(contatti)', link.get('href'))
            #print(link)
            if match.group(0):
    # Check if the link can be input to get_soup function
                stringerContact = link.get('href')
                if stringerContact[:1]=='//': 
                    return 'http:'+stringerContact
                elif stringerContact[0]=='/': # when we have a sublink rather than the full address
                    return stringer+stringerContact
                return stringerContact
         
        except:
            pass
    return ''

def missingData(stringer, soup, listing):
# accepts a list of strings which may have missing data
# returns a list of strings with any additional data available included
    
    # boolean mask for missing information
    missing = [not bool(word) for word in listing]
    if any(missing):
        stringerContact = contact(stringer, soup)
    else:
        stringerContact = ''
    # perform only if the original page has some contactpage 
    # and there is missing information
    #print(stringerContact)
    if bool(stringerContact):
        functions = [email, phone, facebook, instagram]
        try: # in case the contact link on the site is broken
            soupContact = get_soup(stringerContact)
            for idx in [missed for missed in range(4) if missing[missed]]:
    # look only for missing information
                listing[idx] = functions[idx](soupContact)
        except:
            pass
    return listing

def main(stringer):
    soup = get_soup(stringer)
    lister = db(soup)
    listing = [email(soup, lister), phone(lister), facebook(soup), instagram(soup)]

    return dict(zip(['Email: ','Phone: ','Facebook: ','Instagram: '], missingData(stringer, soup, listing)))
  
if __name__=='__main__':
    email, phone, facebook, instagram = main(sys.argv[1])
    print('Email: %s, Phone: %s, Facebook: %s, Instagram: %s' % (email, phone, facebook, instagram))
# python3 pythonScrape.py 'http://diewaid.ch/'
