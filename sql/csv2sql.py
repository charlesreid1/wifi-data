import sqlite3



def csv_to_apclientdata(csv_file):
    """
    Turn a CSV file into 4 lists:
    One list with AP header lines
    One list with AP data lines
    One list of client header lines
    One list with client data lines
    """

    with open(csv_file) as f:
        lines = f.readlines()

    # Find where breaks in CSV file are located
    # (Split between APs and Clients)
    breaks = []
    for i in range(len(lines)):
        tokens = [t.strip() for t in lines[i].split(",")]
        if len(tokens)==1:
            breaks.append(i)

    # Use that to extract ap and client data
    
    ap_header    = lines[breaks[0]+1]
    ap_data      = lines[breaks[0]+2:breaks[1]-1]
    
    client_header = lines[breaks[1]+1]
    client_data   = lines[breaks[1]+2:breaks[2]-1]


    return ap_header, ap_data, client_header, client_data



def print_ap(ap_header,ap_data):

    # Create an sql record for a single AP
    ap = ap_data[1]

    head_tokens = [a.strip() for a in ap_header.split(",")]
    ap_tokens = [a.strip() for a in ap.split(",")]

    record = {}
    for key,val in zip(head_tokens,ap_tokens):
        record[key] = val

    print "-"*30
    print record
    print "-"*30



def print_ap_head(ap_header,ap_data):

    head_tokens = [a.strip() for a in ap_header.split(",")]
    
    print "\'" + "\',\'".join(head_tokens) + "\'"



def make_ap_sql_record(ap_header,ap_data):
    """
    Tokenize the two lists of AP header and data lines
    and extract the data
    """

    # connect to sqlite database
    conn = sqlite3.connect('wifidata.db')

    # get a pointer in the database
    c = conn.cursor()



    # Extract column headers and create table

    head_tokens = [a.strip() for a in ap_header.split(",")]

    ap_head_fields = "\'" + "\',\'".join(head_tokens) + "\'"

    sql_create_table = "CREATE TABLE wifidata (%s)"%(ap_head_fields)

    #print sql_create_table

    try:
        c.execute(sql_create_table)
        print " [+] Success creating table."
    except sqlite3.OperationalError:
        pass

    conn.commit()
    

    # Populate data
    for ap in ap_data:

        ap_tokens = [a.strip() for a in ap.split(",")]

        ap_values = "\'" + "\',\'".join(ap_tokens)+"\'"

        sql_insert = "INSERT INTO wifidata VALUES (%s)"%(ap_values)

        #print sql_insert

        try:
            c.execute(sql_insert)
            print " [+] Success inserting row."
        except sqlite3.OperationalError:
            pass

    conn.commit()

    conn.close()


if __name__=="__main__":

    ap_header, ap_data, client_header, client_data = csv_to_apclientdata('../csv/awesome-01.csv')

    make_ap_sql_record(ap_header,ap_data)

