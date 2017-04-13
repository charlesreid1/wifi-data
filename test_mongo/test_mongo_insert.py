from pymongo import MongoClient
import random

client = MongoClient('localhost', 27017)
db = client.test_database
collection = db.test_collection

docs = [{ 
            'timestamp' : '2017-04-11 11:04:12',
            'bssid' : 'DEADBEEFSFUOESIEWR', 
            'channel' : random.randint(0,100), 
            'ssid' : 'wiiiiiifi', 
            'strength' : -24, 
            'encryption' : 'WPA' 
        },
        {
            'timestamp' : '2017-04-11 11:01:12',
            'bssid' : 'BEEOIEUDSJFLKSDJFF', 
            'channel' : random.randint(0,100), 
            'ssid' : 'iurtiruyiuyrwe',
            'strength' : -20, 
            'encryption' : 'WPA' 
        },
        {
            'timestamp' : '2017-04-11 11:24:12',
            'bssid' : 'BEEF2DJFSKJFLKJSFKJL', 
            'channel' : random.randint(0,100), 
            'ssid' : 'sdfjaskfjlkdfjglfdghfketa', 
            'strength' : -30, 
            'encryption' : 'WPA' 
        }]

result = collection.insert_many(docs)
print result.inserted_ids

