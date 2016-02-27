This folder contains files for converting CSV files to Pandas DataFrames.

## Preliminary Data Processing

### Data Processing Driver

The user will run one Python file, `master_df.py`, in order to process raw CSV data from a wifi data experiment.  
This processes all of the CSV files dumped out during an experiment, and assembles all of them into a single CSV file. 
For extremely large data sets, this step is not feasible to do, and the single, master CSV file would be replaced with a database. 

`master_df.py` is the main driver. Specify your CSV file directory when you run the script:

```
master_df.py ../csv_files/
```

### Data Processing Helper Functions

Functions to help with the process are contained in the file:

`make_df.py` contains the function `make_df()`.
This function splits and extracts data from a single
CSV file and returns two Pandas DataFrames.



## Preliminary Data Analysis

To begin a preliminary data analysis, make sure you have Jupyter notebook installed:

```
$ pip install jupyter
```

Now fire up a Jupyter notebook:

```
$ jupyter notebook
```




















