import sys, os
#Server
#INTERP = '/home/jeanverrette/scrape.jeanverrette.com/bin/python3.5'
#Local
INTERP = '/usr/bin/python3'
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())

#sys.path.append('sample')
from scrapeFlask import app as application
