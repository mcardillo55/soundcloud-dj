#!/usr/bin/env python

from bs4 import BeautifulSoup
from urlparse import urlparse, parse_qs
import subprocess
import requests
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

args = ['casperjs', 'facebook.js']
html = subprocess.check_output(args)

soup = BeautifulSoup(html, 'html.parser')
soup = soup.find(id='contentArea')
allHref = soup.findAll(href=True)

urlList = []
for href in allHref:
    fb_u = parse_qs(urlparse(href['href']).query).get('u')
    if fb_u:
        if fb_u[0] not in urlList:
            urlList.append(fb_u[0])
            r = requests.post(config.HOSTNAME + '/api/songs/',
                {'token': config.SECRET_KEY, 'url': fb_u[0]})
            print fb_u[0]
            print r.text
