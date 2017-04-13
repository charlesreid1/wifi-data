from datetime import datetime
import os, re
from pymongo import MongoClient


def main():

    client = MongoClient('localhost',27017)
    
    # get (create) wifi database
    db = client.wifi
    
    # get (create) wifi collection
    apcol = db.ap_data
    clientcol = db.client_data
    
    files = os.listdir('/wifi')
    
    for relative_filename in os.listdir('/wifi'):
        
        # extract ap and client info from the csv file
        csv_file = '/wifi/'+relative_filename
        ap, client = parse_ap_client_data(csv_file)

        if len(ap)>0:
            result1 = apcol.insert_many(ap)
        if len(client)>0:
            result2 = clientcol.insert_many(client)

        print ""
        print "-"*30
        print "Processing wifi data from csv file %s"%(csv_file)
        print "Success:"
        print result1.inserted_ids
        print result2.inserted_ids

    print ""
    print "-"*30
    print "All done!"


def parse_ap_client_data(csv_file):
    """
    This reads the given CSV file, 
    splits the AP and client information,
    parses data from each column,
    and creates a set of MongoDB records.

    It returns two lists of dictionaries
    ready to be inserted into a MongoDB database.
    """

    # get the hostname of the device that captured this data
    host = re.split(r'[^a-zA-Z0-9]{1,}', csv_file)[0]

    with open(csv_file,'r') as f:
        contents = f.readlines()

    # strip whitespace from all lines
    contents = [z.strip() for z in contents]

    # find blank lines:
    blank_lines = [i for i,z in enumerate(contents) if z=='']
    


    # ======================================================
    # Access Points:

    # get start and end range
    if len(blank_lines) > 1:
        start = blank_lines[0]
        finish = blank_lines[1]
    else:
        start = 0
        finish = blank_lines[0]

    # create list that will store all AP info in the file contents
    ap_contents = []

    # add access point 
    for i in range(start,finish):
        ap_contents.append( contents[i] )
    


    # extract ap data from raw file contents

    ap_documents = []
    for j,txt in enumerate(ap_contents):
        if txt<>'' and j>1:

            data = [t.strip() for t in txt.split(",")]

            ap_document = {}
            ap_document['bssid'] = data[0]
            ap_document['time'] = datetime.strptime(data[1], "%Y-%m-%d %H:%M:%S")
            ap_document['channel'] = int(data[3])
            ap_document['privacy'] = data[5]
            ap_document['cipher'] = data[6]
            ap_document['authentication'] = data[7]
            ap_document['power'] = int(data[8])
            ap_document['nbeacons'] = int(data[9])
            ap_document['essid'] = data[13]
            ap_document['host'] = host

            ap_documents.append(ap_document)




    # ======================================================
    # Clients:

    # List to hold all lines from file containing info about clients
    client_contents = []

    # get start and end range
    if len(blank_lines) > 1:
        start = blank_lines[1]
        finish = blank_lines[2]
    else:
        start = blank_lines[0]
        finish = len(contents)

    # populate content with start to finish
    for i in range(start, finish): 
        client_contents.append( contents[i] )

    # extract client data from raw file contents

    client_documents = []
    for j,txt in enumerate(client_contents):
        # the j>1 excludes the first empty line and the CSV file header
        if txt<>'' and j>1:

            data = [t.strip() for t in txt.split(",")]

            client_document = {}
            client_document['mac'] = data[0]
            client_document['time'] = datetime.strptime(data[1], "%Y-%m-%d %H:%M:%S")
            client_document['power'] = int(data[3])
            client_document['npackets'] = int(data[4])
            client_document['bssid'] = data[5]
            client_document['host'] = host

            client_documents.append(client_document)


    # ======================================================
    # Return AP and client wifi data,
    # ready to be inserted into the mongodb

    return ap_documents, client_documents


if __name__=="__main__":
    main()

