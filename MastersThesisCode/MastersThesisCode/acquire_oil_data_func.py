import csv
import os
import polars as pl
import yfinance as yahoo
from statsmodels.tsa.stattools import adfuller
from file_operations import file_existence_check, export_values_to_csv

# Function for if the user wishes to re-acquire fresh data using the list of stocks
def acquire_oil_data():

    # Establishing the directory path for all files for this project
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Establishing the dataframe for the stock data
    oil_data = {}
    
    # Acquire Crude Oil Price, July 1st, 2012 was a Sunday, so the first return will be on July 2nd, and July 1, 2024 was a Monday, so it will be included
    yahoo_df = yahoo.download("CL=F", start = "2012-06-29", end = "2024-07-02", progress = False, auto_adjust = True)
    yahoo_df = yahoo_df.reset_index()
    if yahoo_df.empty == False:
        oil_data = pl.from_pandas(yahoo_df)
        oil_data = oil_data.rename({f"('Date', '')":"Date_CL=F", f"('Close', 'CL=F')":"Close_CL=F"})
        oil_data = oil_data.drop(pl.exclude(["Date_CL=F", "Close_CL=F"]))
    else:
        print(f"No Crude Oil Price Data Found.")
        
    oil_data = oil_data.with_columns([(pl.selectors.by_index([1]).diff()).alias(f"Diff_CL=F")])
    oil_data = oil_data.select(pl.all().slice(1))
    
    print(oil_data)
    
    # Seeing if the concat  and average files exist first, and deletes the existing one
    file_existence_check(f"{script_dir}\Data\oil_data.csv")

    # Exporting the new .csv files
    export_values_to_csv('oil_data.csv', oil_data)

    # Returning the oil data with regular returns
    return oil_data

# Checks the stationarity of a particular set of stock averages
def check_stationarity_oil(oil):
    adf = adfuller(oil["Diff_CL=F"])
    print(f"P-value: {adf[1]}")

    # Confirming stationarity or non stationarity
    if adf[1] < 0.05:
        print("Log values ARE stationary")
        return True
    else:
        print("Log values are NOT stationary.")
        return False