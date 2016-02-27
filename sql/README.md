This folder contains files for converting CSV files to SQL records.

### Driver

The user will run one Python file: 

`process_csv_files.py` is the main driver. Specify your CSV file directory when you run the script:

```
process_csv_files.py ../csv_files/
```

### Functions

Functions to help with the process are contained in two Python files:

`extract_csv_data.py` contains the function `extact_csv_data()`. 
This function splits and extracts airodump CSV file data and returns
lists of strings. 

`make_sql_record.py` contains two functions: one to turn access point observations
into SQL records, and one to turn client observations into SQL records.


