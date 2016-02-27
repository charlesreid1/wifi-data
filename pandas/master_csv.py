import os
import sys
import pandas as pd
from make_df import make_df

"""
master_csv.py



Usage:

    $ python master_csv.py [path to csv files]

This script turns a pile of CSV files into two master DataFrames,
one for access point (AP) data and one for client data,
then dumps out those master DataFrames into CSV files. 
The end result is, the entire experiment is contained in two
CSV files that are much easier to load into memory with Pandas.



Why is this script necessary?

Normally, if we were dealing with a large sensor network, 
we would want to use a database to store all of our data.
In place of a master DataFrame, we would have a database.

But because our data set is small enough, we can deal with
Pandas and other CSV files directly.



How does it work?

This script processes CSV files one-by-one. 
Each CSV file is turned into two DataFrames (AP and client data).

The code to process, split, and tokenize the CSV files and turn them
into Pandas DataFrames is in make_df.py.

The code to turn the extracted CSV data into SQL records 
is in make_sql_record.py.
"""



def main(csv_directory):
    """
    This is the main driver program.
    """

    # Get a list of CSV file names
    csv_files = []
    for some_file in os.listdir(csv_directory):
        if some_file[-4:]=='.csv':
            csv_files.append(some_file)

    if csv_files == []:
        print("\n\nERROR: No CSV files found in folder %s\n"%(csv_directory))
        sys.exit(1)

    ap_df = pd.DataFrame([])
    client_df = pd.DataFrame([])

    i=0
    for csv_file in csv_files:

        #print("Extracting data frame from %s"%(csv_file))

        next_ap_df, next_client_df = make_df(csv_directory+'/'+csv_file) 

        ap_df = ap_df.append(next_ap_df,ignore_index=True)
        client_df = client_df.append(next_client_df,ignore_index=True)

        a = 0
        i=i+1

    print("Finished extracting all data.")

    print("Access point data frame contains %d observations"%(ap_df.shape[0]))
    print("Client data frame contains %d observations"%(client_df.shape[0]))

    ap_df_file = 'data_ap.csv'
    client_df_file = 'data_client.csv'

    ap_df.to_csv(ap_df_file,index=False) 
    client_df.to_csv(client_df_file,index=False)

    print("Finished creating master CSV files %s and %s."%(ap_df_file,client_df_file))



def usage():
    """
    Help the user out
    """
    print("\n----------------------------")
    print("Wifi Data Project")
    print("Master CSV Script")
    print("Usage:\n")
    print("  $ python master_csv.py [location of csv files]\n")
    print("Specify the location of your CSV files on the command line.")
    print("For example, if my CSV files are in /foo/bar, I should run:\n")
    print("  $ python master_csv.py /foo/bar")
    print("\n----------------------------")



if __name__=="__main__":
    """
    Python's version of public static void main()
    """
    
    # User needs to provide 1 argument
    if len(sys.argv)!=2:
        usage()
        sys.exit(1)

    # 1 argument is CSV directory
    csv_directory = sys.argv[1]
    
    # Make sure it is a directory
    if (os.path.isdir(csv_directory)!=True):
        print("\n\nERROR: %s is not a directory.\n"%csv_directory)
        usage()
        sys.exit(1)

    main(csv_directory)


