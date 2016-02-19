import os
import sqlite3


class Stuff(object):
    def __init__(self):
        pass




def make_ap_sql_record(ap_header,ap_data):
    """
    Tokenize the two lists of AP header and data lines
    and extract the data

    Here are the usual fields, for reference:

    0  BSSID = string
    1  First time seen = string
    2  Last time seen = string
    3  Channel = int
    4  Speed = int
    5  Privacy = string
    6  Cipher = string
    7  Auth = string
    8  Power = int
    9  # beacons = int
    10 # iv = int
    11 lan ip = string 
    12 id-length = int
    13 essid = string
    14 key = string 
    """

    db_file = 'wifidata.db'

    # Check if database exists/if table needs to be created
    print("Kiss it goodbye.")
    os.system('rm -f %s'%(db_file))



    # Tokenize the AP column headers (i.e., chop it up at the commas)
    # This returns a list of tokens.
    # These tokens will become field names for the the AP data SQL records.
    ap_header_tokens = [a.strip() for a in ap_header.split(",")]




    # connect to sqlite database
    conn = sqlite3.connect(db_file)

    # get a pointer in the database
    c = conn.cursor()



    # ---------
    # We have to create the SQL tables,
    # which means we have to figure out the data type of each column.

    # First, assemble a list of columns
    # (and a list of columns that need special treatment)

    # datetime columns
    datetime_columns = ['First time seen','Last time seen']
    datetime_ix = [ap_header_tokens.index(z) for z in datetime_columns]

    # integer columns
    integer_columns = ['channel','Speed','Power','# beacons','# IV']
    integer_ix = [ap_header_tokens.index(z) for z in integer_columns]

    # drop columns
    drop_columns = ['LAN IP','ID-length','Key']
    drop_ix = [ap_header_tokens.index(z) for z in drop_columns]



    # Now assemble a dictionary 
    # with keys of column names and values of SQL data type
    # (for sqlite data types, see https://www.sqlite.org/datatype3.html)

    types = {}


    for key in ap_header_tokens:
        
        if key in datetime_columns:
            # we have a datetime type, 
            # so deal with it.
            types[key] = 'DATETIME'

        elif key in integer_columns:
            # we have an integer type,
            # so deal with it.
            types[key] = 'INTEGER'

        elif key in drop_columns:
            # drop this column
            pass

        else:
            types[key] = 'TEXT'


    if (os.path.isfile(db_file)!=True):

        print("Creating table...")

        # Create a table, specifying types
        sql_create_table = "CREATE TABLE wifidata(" 
        for key in types.keys():
            value = types[key]
            # print the column name surrounded by single quotes, 
            # then print its type (date/integer/text/etc)
            sql_create_table += "'%s' %s,"%(key,value)

        # remove the last comma
        sql_create_table = sql_create_table[:-1]

        # close the SQL create table statement
        sql_create_table += ")"

        ## Double check this SQL create table statement makes sense
        #print(sql_create_table)

        # it should be something like
        # CREATE TABLE wifidata( column_name1 TEXT, column_name2 INTEGER, column_name3 DATETIME ) 

        c.execute(sql_create_table)

    else:
        print("Skipping table creation...\n")

    # Done creating the table.
    # ---------



    # ---------
    # Insert data, using proper types

    for ap_dat in ap_data:

        # INSERT INTO wifidata(key1, key2, key3) VALUES(v1, v2, v3)

        sql_insert = "INSERT INTO wifidata("
        for key in types.keys():
            sql_insert += "\'" + key + "\',"
        
        # remove last comma
        sql_insert = sql_insert[:-1]
        sql_insert += ") VALUES ("

        for key in types.keys():
            column_type = types[key]
            ix = ap_header_tokens.index(key)
            ap_tokens = [z.strip() for z in ap_dat.split(",")]

            if column_type=='DATETIME':
                value_string = "date('%s')"%(ap_tokens[ix])

            elif column_type=='INTEGER':
                value_string = ap_tokens[ix]

            elif column_type=='TEXT':
                value_string = "\'"+stripslashes(ap_tokens[ix])+"\'"

            sql_insert += value_string + ","

            #print("%s : %s [%s]"%(key,value,column_type))

        sql_insert = sql_insert[:-1]
        sql_insert += ")"

        print sql_insert

    #conn.commit()

    conn.close()

    # now populate SQL db with rows of AP data 

    a = 0


def make_client_sql_record(client_header,client_data):
    pass




