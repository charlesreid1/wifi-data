import os
import sys
from make_df import make_df

"""
load_stuff.py

Usage:

    $ python load_stuff.py [path to csv files]

This turns CSV files into Pandas DataFrames for easier analysis.

Each CSV file is turned into two DataFrames, one for 
access point (AP) data and one for client data.

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

    i=0
    for csv_file in csv_files:
        print("Extracting data frame from %s"%(csv_file))
        ap_df, client_df = make_df(csv_directory+'/'+csv_file) 
        print client_df.shape
        i=i+1

    print("Finished extracting all data.")



def usage():
    """
    Help the user out
    """
    print("\n----------------------------")
    print("Wifi Data Project")
    print("Process CSV Files Script")
    print("Usage:\n")
    print("  $ python process_csv_files.py [location of csv files]\n")
    print("Specify the location of your CSV files on the command line.")
    print("For example, if my CSV files are in /foo/bar, I should run:\n")
    print("  $ python process_csv_files.py /foo/bar")
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

