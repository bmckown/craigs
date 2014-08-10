#!/usr/bin/python

from twilio.rest import TwilioRestClient
from pprint import pprint
import unicodedata
import feedparser
import sqlite3
import email
import time
import sys
import re

def stringify(text):
    return u"\'" + unicode(text) + u"\'"

def insert(item):
    pid = item["id"]
    title = item["title"]
    summary = item["summary"]
    link = item["link"]
    published = item["published"]
    insert_statement = u"INSERT OR IGNORE INTO cl_item_list VALUES (" + u",".join(map(stringify,[pid,title,summary,link,published])) + u")"
    return unicodedata.normalize('NFKD', insert_statement).encode('ascii','ignore')

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
            select = c.execute("SELECT * FROM cl_item_list WHERE id = ?", (item['id'],))
            if select is None:
                print select
            else:
                c.execute("INSERT INTO cl_item_list VALUES (?,?,?,?,?)" , (item['id'], item['title'], item['summary'], item['link'], item['published']))
                print "NEW ITEM" 
        conn.commit()
        time.sleep(6)
    except KeyboardInterrupt as e:
        break

conn.close()


