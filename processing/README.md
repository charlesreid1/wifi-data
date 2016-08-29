# Processing

Steps for processing Aircrack data:
* Clean the CSV data (split it into client and AP data for easier parsing)
* Load the data into Pandas DataFrame for inspection/further cleaning
* Use Pandas/Bokeh to start visualizing simple quantities
* Increase complexity from there

## Cleaning Aircrack CSV Data

The Aircrack tool outputs lots of information in its CSV files.
However, these combine client and AP data together.
It is more useful for us to separate client and AP data,
so we can analyze them separaately.

`clean_csv.py` script:
* Python script for munging text files
* Looks for CSV files from Aircrack in current directory
* Aircrack CSV files are read in and split into AP data and client data
* New CSV files corresponding to AP data and client data are written


