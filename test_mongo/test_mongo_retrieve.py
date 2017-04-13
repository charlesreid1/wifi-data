from pymongo import MongoClient
import random

client = MongoClient('localhost', 27017)
db = client.test_database
collection = db.test_collection

# Note: 
# The space in front of the askterisk is important. 
# (Got it working through trial and error: W* worked, *A didn't, so * as leading character led to problems.)
for doc in collection.find({'encryption':{'$regex':' *'}}):
    print "Channel: %d \tNetwork bssid: %s"%( doc['channel'], doc['bssid'] )


