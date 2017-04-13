import sqlite3
import time
import string
import random


# connect to sqlite database
conn = sqlite3.connect('wifidata.db')

# get a pointer in the database
c = conn.cursor()


# https://www.sqlite.org/lang_datefunc.html

try:
    c.execute("CREATE TABLE wifidata (device_key, device_mac, last_seen)")
except sqlite3.OperationalError:
    print "Error creating table. Continuing..."
    pass





       
        # now insert 60 random records into the database
        for z in range(60):
                time.sleep(1)
        
                random_key = id_generator(size=8)
                random_mac = mac_generator()
                random_strength = random.randint(1,100)
        
                print &quot;Inserting record (%s,&#160;%s,&#160;%d)&quot;%(random_key, random_mac, random_strength)
        
                c.execute( &quot;INSERT INTO wifidata VALUES ('%s', '%s',&#160;%d);&quot;%(random_key, random_mac, random_strength) )
        
                # save (commit) the changes
                conn.commit()
        
        # close the connection
        conn.close()

