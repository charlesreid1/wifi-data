This folder contains files for converting CSV files to SQL records.

### Driver

The user only needs to run one Python file, the driver, which is `process_csv_files.py`. When you run the script, you specify the location of your csv files:

```
$ process_csv_files.py ../csv_files/
```

This driver will call functions contained in other files.

### Functions

Functions to help with the process are contained in two Python files:

`extract_csv_data.py` contains the function `extact_csv_data()`function `extact_csv_data()`. 
This function splits and extracts airodump CSV file data and returns
lists of strings. 

`make_sql_record.py` contains two functions: one to turn access point observations
into SQL records, and one to turn client observations into SQL records.


