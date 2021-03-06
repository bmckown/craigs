#!/usr/bin/python

import feedparser
import sqlite3
import smtplib 
import time
import json
import sys

config_file = sys.argv[1]
with open(config_file,"rb") as cf:
    config = json.loads(cf.next().strip())


conn = sqlite3.connect(config['db'])
base_url = config['rss_feed'] 
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
            check = select.fetchone()
            if check is None:
                important = (item['id'], item['title'], item['summary'], item['link'], item['published'])
                c.execute("INSERT INTO cl_item_list VALUES (?,?,?,?,?)" , important)
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(config["email"],config["email_password"])
                server.sendmail(config["email"],config["email_to"], ", ".join(important).encode("utf-8").strip())
                server.quit()
        conn.commit()
        time.sleep(60*10)
    except KeyboardInterrupt as e:
        break

conn.close()


