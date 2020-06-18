soundcloud-dj
=============

Live at https://www.michaeljcardillo.com/scdj

Allow users to create global soundcloud + youtube playlists

But mostly just screwing around with Angular.JS & Flask a bit

## Installation

**Use Python 2 ONLY**

### Install Requirements
`pip install -r ./requirements.txt`

### Initialize DBs
`python ./db_create.py`

### Run gevent/socketio server
`python ./run.py`

Site will be available locally at 127.0.0.1:5000. The flask_socketio server is production ready so you can deploy this server to production by reverse proxying to this address.

## Note
The scraping scripts provided in ./tools/ are currently broken due to a bug in phantomjs, which is no longer in development. They will need to be rewritten to use another headless browser.
