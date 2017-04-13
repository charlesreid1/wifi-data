import os
import sqlite3
from oops import oops


def make_ap_sql_record(ap_header,ap_data):
    """
    Tokenize the two lists of AP header and data lines
    and extract the wifi data

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


    try:

        print("Creating table...")

        # Create a table, specifying types
        sql_create_table = "CREATE TABLE apdata(" 
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
        # CREATE TABLE apdata( column_name1 TEXT, column_name2 INTEGER, column_name3 DATETIME ) 

        c.execute(sql_create_table)

    except sqlite3.OperationalError:
        print("Skipping table creation...\n")

    # Done creating the table.
    # ---------



    # ---------
    # Insert AP data into SQL database, using proper types

    for ap_dat in ap_data:

        # Final statement will look like this:

        # INSERT INTO apdata(key1, key2, key3) VALUES(v1, v2, v3)


        sql_insert = 'INSERT INTO apdata('

        # add the name of each column
        for key in types.keys():
            sql_insert += "\'" + key + "\',"

        # remove that last comma
        sql_insert = sql_insert[:-1]
        sql_insert += ") VALUES ("


        # print out the data differently - depending on its type
        for key in types.keys():
            column_type = types[key]
            ix = ap_header_tokens.index(key)
            ap_tokens = [z.strip() for z in ap_dat.split(",")]

            if column_type=='DATETIME':
                value_string = "date('%s')"%(ap_tokens[ix])

            elif column_type=='INTEGER':
                value_string = ap_tokens[ix]

            elif column_type=='TEXT':
                temp_string = ap_tokens[ix]
                temp_string = temp_string.replace('\"','')
                #temp_string = temp_string.replace('\\','\\')
                temp_string = temp_string.replace('\'','')

                value_string = "'"+temp_string+"'"

            sql_insert += value_string + ","

        # remove last comma
        sql_insert = sql_insert[:-1]
        sql_insert += ")"

        print sql_insert

        conn.execute(sql_insert)

    conn.commit()

    conn.close()

    # Done inserting AP data into SQL database.
    # ---------





def make_client_sql_record(client_header,client_data):
    """
    Tokenize the two lists of client header and client data lines
    and extract the wifi data
    """

    db_file = 'wifidata.db'



    # Tokenize the AP column headers (i.e., chop it up at the commas)
    # This returns a list of tokens.
    # These tokens will become field names for the the AP data SQL records.
    client_header_tokens = [c.strip() for c in client_header.split(",")]


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
    datetime_ix = [client_header_tokens.index(z) for z in datetime_columns]

    # integer columns
    integer_columns = ['Power','# packets']
    integer_ix = [client_header_tokens.index(z) for z in integer_columns]

    drop_columns = []


    # Now assemble a dictionary 
    # with keys of column names and values of SQL data type
    # (for sqlite data types, see https://www.sqlite.org/datatype3.html)

    types = {}

    for key in client_header_tokens:
        
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


    try:

        print("Creating table...")

        # Create a table, specifying types
        sql_create_table = "CREATE TABLE clientdata(" 
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
        # CREATE TABLE apdata( column_name1 TEXT, column_name2 INTEGER, column_name3 DATETIME ) 

        c.execute(sql_create_table)

    except sqlite3.OperationalError:
        print("Skipping table creation...\n")

    # Done creating the table.
    # ---------


    # ---------
    # Insert AP data into SQL database, using proper types

    for client_dat in client_data:

        # Final statement will look like this:

        # INSERT INTO clientdata(key1, key2, key3) VALUES(v1, v2, v3)


        sql_insert = 'INSERT INTO clientdata('

        # add the name of each column
        for key in types.keys():
            sql_insert += "\'" + key + "\',"

        # remove that last comma
        sql_insert = sql_insert[:-1]
        sql_insert += ") VALUES ("


        # print out the data differently - depending on its type
        for key in types.keys():
            column_type = types[key]
            ix = client_header_tokens.index(key)
            client_tokens = [z.strip() for z in client_dat.split(",")]

            if len(client_tokens) > len(client_header_tokens):
                tmp = client_tokens[0:len(client_header_tokens)-1]
                last = ','.join( client_tokens[len(client_header_tokens)-1:] )
                client_tokens = tmp + [last]

            if column_type=='DATETIME':
                value_string = "date('%s')"%(client_tokens[ix])

            elif column_type=='INTEGER':
                value_string = client_tokens[ix]

            elif column_type=='TEXT':
                try:
                    temp_string = client_tokens[ix]
                    temp_string = temp_string.replace('\"','')
                    temp_string = temp_string.replace('\'','')

                    value_string = "'"+temp_string+"'"
                except IndexError:
                    pass

            sql_insert += value_string + ","




if __name__=="__main__":
    oops()

