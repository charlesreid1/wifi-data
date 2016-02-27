This folder contains files for converting CSV files to Pandas DataFrames.

### Driver

The user will run one Python file: 

`load_stuff.py` is the main driver. Specify your CSV file directory when you run the script:

```
load_stuff.py ../csv_files/
```

### Functions

Functions to help with the process are contained in the file:

`make_df.py` contains the function `make_df()`.
This function splits and extracts data from a single
CSV file and returns two Pandas DataFrames.

