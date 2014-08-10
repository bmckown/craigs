#!/usr/bin/python

from twilio.rest import TwilioRestClient
import feedparser
import sqlite3
import email
import time
import sys

conn = sqlite3.connect("cl_list.db")

base_url = "http://austin.craigslist.org/search/sss?query=jute%20rug&s=0&sort=rel&format=rss"

c = conn.cursor()

try:
    c.execute('''CREATE TABLE cl_item_list 
             (id text, title text, summary text, link text, date_published text )''')
    conn.commit()
except:
    pass

#Example of how to insert data into the db 
#c.execute('''INSERT INTO cl_item_list VALUES ('www.craigslist.com/id2','Jute Rug','Its a rug made of jute','www.craigslist.com/id2','yesterday')''')

while True:
    try:
        sys.stderr.write("Fetching " + base_url + "\n")
        parsed = feedparser.parse(base_url)
        for item in parsed["items"]:
            
        time.sleep(60*10)
    except KeyboardInterrupt as e:
        break

conn.close()


