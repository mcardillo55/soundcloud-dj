#!/usr/bin/env python

from BeautifulSoup import BeautifulSoup
from urlparse import urlparse, parse_qs
import subprocess
import requests

args = ['phantomjs', 'facebook.js']
html = subprocess.check_output(args)

soup = BeautifulSoup(html)
soup = soup.find('div', {'id':'contentArea'})
allHref = soup.findAll(href=True)

urlList = []
for href in allHref:
    fb_u = parse_qs(urlparse(href['href']).query).get('u')
    if fb_u:
        if fb_u[0] not in urlList:
            urlList.append(fb_u[0])
            r = requests.post('http://www.shipfamradio.com/api/songs/',
                {'token': 'secret', 'url': fb_u[0]})
            print fb_u[0]
            print r.text

