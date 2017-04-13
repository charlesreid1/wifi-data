import os
import sys
from extract_csv_data import extract_csv_data
from make_sql_record import make_ap_sql_record, make_client_sql_record

"""
process_csv_files.py

Usage:

    $ python process_csv_files.py [path to csv files]

This turns CSV files into SQL records and puts them into the file wifidata.db.

It automatically splits the CSV file into AP data and client data,
extracts field names, and creates SQL records for each line in the 
CSV file.

The code to process, split, and tokenize the CSV files is 
in extract_csv_data.py.

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

    for csv_file in csv_files:

        print("Extracting data from %s"%(csv_file))

        ap_header, ap_data, client_header, client_data = extract_csv_data(csv_directory+'/'+csv_file)

        # Turn the AP data into SQL records
        make_ap_sql_record( ap_header, ap_data )

        # Turn the client data into SQL records
        make_client_sql_record( client_header, client_data )

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

