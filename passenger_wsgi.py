import sys, os
INTERP = '/home/jeanverrette/scrape.jeanverrette.com/bin/python3.5'
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())

#sys.path.append('sample')
from hello import app as application