<html>
    <head>
        <meta charset="UTF-8"> 
<style>
code { 
    font-family: monospace;
}
</style>
        <title>Scraper</title>
    </head>
    <body>
        <h1>Simple Website Scraper</h1>
<h1>Give me a website address.</h1>
    <form method='POST', action="/">
        <div class='form-group'>
            <input type="text" name="website">
        </div>
        <input class="btn btn-primary" type="submit" value="submit">
    </form>

<p>In this tutorial, we display the use of regexes and beautiful soup to scrape information from websites. Rather than explain each detail of the necessary code, we present the fundamental and novel pieces that the reader may find interesting. Readers interested in reproducing the app are encouraged to visit the full github code for more information.</p>

<h3>Dependencies</h3>
<p>We've excuted the app with Python 3.5 and modules re, urllib3, and bs4. While any version of python 3 will already be equipped with re, the latter modules can be installed with pip.</p>

<code>
  $pip install urllib3<br>
  $pip install beautifulsoup4
</code>

<h3>Re</h3>
<p>We've used regular expressions to pull key pieces of contact information from the text of the website. Many of the regex patterns we've used in our algorithm are reviewed below, but we encourage interested parties to visit the Python documentation for more information.</p>
<a href="https://docs.python.org/3/library/re.html">link text</a>

<p>The re.search function gives us a match whose information can be assessed using match.group</p>
<code>
   $match = re.search('instagram', 'https://www.instagram.com/')
   $match.roup(0)
</code>

<p>When applying re.search to links on the given website, we searched for the first link that includes the word facebook.</p>

<code>
   $match = re.search('facebook', link)
   $facebookLink = match.group(0)
</code>

<p>Different regrex functions were written based on the country of origin of any phone number.
Indiviual characters put inside [], square brackets, match any of the individual characters. When considering phone numbers, we would like to match both <br>
867-5309<br>
<a href="https://www.youtube.com/watch?v=mDC_2zTrpbg">867 5309</a><br>
Hence, we will utilize [ -] in our algorithm.</p>

<p>We would also like to match numbers calling long distance or locally.<br>
1 (415) 523-0057<br>
<a href="https://www.crunchbase.com/organization/fake-number-club#section-overview">(415) 523-0057</a><br>
The question mark, ?, to the right of some character(s) matches exactly 0 or 1 repititions of the character(s). Hence, we will utilize 1? in our algorithm.</p>

<p>While \w matches any alphanumeric character, \d matches any digit 0-9.  Because we were looking for blocks of 3 or 4 digits, we utilized \d{3} or \d{4}.</p>

<p>We chose to create separate regexes based on the country. Our algorithm will only detects phone numbers from those countries.</p>

<code>
<?php
   $str = "$usa = '(1|\+1)?([ -])?(\d{3}|\(\d{3}\))?([ -])?\d{3}([ -])?\d{4}'";
echo htmlspecialchars($str);
?><br>
<?php
   $str = "$swiss = '(41|\+41)?(0|\(0\))?\d{2}([ -])?\d{3}([ -])?\d{2}([ -])?\d{2}'";
echo htmlspecialchars($str);
?><br>
<?php
   $str = "$china = '(86|\+86)?([ -])?1\d{2}([ -])?\d{4}([ -])?\d{4}'";
echo htmlspecialchars($str);
?><br>
</code>

<h3>Beautiful Soup</h3>
<p>The <a href="https://www.crummy.com/software/BeautifulSoup/bs4/doc/">Beautiful Soup</a> module was used to parse the given website's html. We use urllib3 and a get request to recover the html, and beautiful soup organizes everything to make it easy to search by html tags. </p>

<h3>Recovering and Searching Links from website</h3>
<p>We begin by pulling out all of the <\a> tags.</p>
 
<code>
   $links = soup.find_all('a')
</code>
<p>For each link, we can search for pertinent substrungs using the re module as described previously.</p>


<code>
            match = re.search('mailto:', link.get('href'))
            if match.group(0):
                output = link.get('href')
                return output.replace("mailto:", "")
        except:
            pass

</code>

<p>Note that the try and except flow controls are necessary, because re.search may not always run successfully. Because only some websites link the email address with the 'mailto:' substring, we must also use a regex on the text from the website.</p>


<code>
<?php
   $str = "'(<)?(\w+@\w+(?:\.\w+)+)(?(1)>)'";
echo htmlspecialchars($str);
?> 
</code>
<h3>Visible text from the website</h3>
<p>The beautifulsoup get_text function does not respect <\br> tags within the html. We replace such tags with newlines so that contact information on separate lines do not blend together.</p>

<code>
<?php
   $str = "$output = str(page.data).replace("<br/>", '\n')";
echo htmlspecialchars($str);
?>
</code>
We proceed by removing many of the hidden tags from the soup of html.
soup = BeautifulSoup(output, "lxml")

<code>
   $[s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
</code>
<p>Applying the get_text function to the entire beautiful soup variable, results in phrases and text running together without proper spacing. To combat this, we consider only the <\p> tags, and apply get_text to each of the contents.</p>

<code>

   $contents = soup.find_all("p")
   $outputText = [content.get_text() for content in contents]
   # split up the list further based on new lines or tabs
   # having various lines will make it easier to distinguish 
   # between important information and various words
   $lister = []
   $for phrase in outputText:
<?php
   $str = "lister.extend(phrase.split("\n"))";
echo htmlspecialchars($str);
?>

</code>
<p>For example, we don't want foul cases like the one below.<br/>
1600 Pennsylvania Avenue NW<br/>
Washington, DC 20500<br/>
<a href="https://twitter.com/realDonaldTrump">202-456-1111</a></p>

<code>
<?php
   $str = "$htmlstring = '<html><head> </head><body></a>1600 Pennsylvania Avenue NW<br/>Washington, DC 20500<br/>202-456-1111</a></body></html>'";
echo htmlspecialchars($str);
?><br>
   $soup = BeautifulSoup(html, 'lxml')<br>
   $soup.get_text()<br>
   :'1600 Pennsylvania Avenue NWWashington, DC 20500202-456-1111'

</code>

<h3>Contact Page</h3>
<p>Many webpages include particular contact information pages. Our code performs the same search algorithm on the contact page if and only if both a contact page exists, and all contact information was not previously found on the original webpage. </p>

<p>Out regular expression matches contact pages in English, French, German, and Italian.</p>

<code>

   $match = re.search('(contact)|(kontakt)|(contatti)', link.get('href'))
</code>
<p>We run into two major error cases when considering contact page urls.
Case 0. The protocol of the url is not given.
Case 1. Only the path of the contact page url is given.</p>


<code>

   $def contact(stringer, soup):
   # stringer is the original websites
   # soup is the beautiful soup variable resulting from the original website
   ...
                if stringerContact[:1]=='//': 
                    return 'http:'+stringerContact
                elif stringerContact[0]=='/': # when we have a sublink rather than the full address
                    return stringer+stringerContact

</code>
<p>We will not include any further information about <a href="http://flask.pocoo.org/">Flask</a> or <a href="https://www.phusionpassenger.com">Passenger</a> used to display this tutorial.
Please visit the github package for the complete code and more information. Email any further questions to <a href="mailto:jverrette@gmail.com">jverrette@gmail.com</a>, and thank you for reading!</p>
    </body>
</html>
