# This python script performs the same php function
# htmlspecialchars which converts regular strings of special characters into characters that can be viewed in html
#
import sys, html

def main():
    output = []
    output.append(html.escape("<\br>"))
    output.append(html.escape("<\p>"))
    output.append(html.escape("= '(1|\+1)?([ -])?(\d{3}|\(\d{3}\))?([ -])?\d{3}([ -])?\d{4}'"))
    output.append(html.escape("= '(41|\+41)?(0|\(0\))?\d{2}([ -])?\d{3}([ -])?\d{2}([ -])?\d{2}'"))
    output.append(html.escape("= '(86|\+86)?([ -])?1\d{2}([ -])?\d{4}([ -])?\d{4}'"))
    output.append(html.escape("$germany = '(49|\+49)?([ -])?(\d{3}|\(\d{3}\))?([ -])?\d{3}([ -])?\d{4}'"))
    output.append(html.escape("$uk = '\(?0\d{2,3}\)?([ -])?\d{3,4}([ -])?\d{4}'"))
    output.append(html.escape("'(<)?(\w+@\w+(?:\.\w+)+)(?(1)>)'"))
    output.append(html.escape("$output = str(page.data).replace('<br/>', '\n')"))
    output.append(html.escape("lister.extend(phrase.split('\n'))"))
    output.append(html.escape("$htmlstring = '<html><head> </head><body></a>1600 Pennsylvania Avenue NW<br/>Washington, DC 20500<br/>202-456-1111</a></body></html>'"))
    return output

if __name__=='__main__':
    for phrase in main():
        print('%s' % (phrase))
