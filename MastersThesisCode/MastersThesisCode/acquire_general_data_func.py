import os
import polars as pl
import yfinance as yahoo
import numpy as np
from statsmodels.tsa.stattools import adfuller
from file_operations import file_existence_check, export_values_to_csv
from datetime import datetime

# Function for if the user wishes to re-acquire fresh data using the list of stocks
def acquire_general_data(stock_ticker, averaged_stocks):

    # Establishing the directory path for all files for this project
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Establishing the dataframe for the stock data
    stock_data = {}
    
    # Acquire Crude Oil/S&P500 Price, July 1st, 2012 was a Sunday, so the first return will be on July 2nd, and July 1, 2024 was a Monday, so it will be included
    yahoo_df = yahoo.download(stock_ticker, start = "2012-06-29", end = "2024-07-02", progress = False, auto_adjust = True)
    yahoo_df = yahoo_df.reset_index()
    if yahoo_df.empty == False:
        stock_data = pl.from_pandas(yahoo_df)
        stock_data = stock_data.rename({f"('Date', '')":f"Date_{stock_ticker}", f"('Close', '{stock_ticker}')":f"Close_{stock_ticker}"})
        stock_data = stock_data.drop(pl.exclude([f"Date_{stock_ticker}", f"Close_{stock_ticker}"]))
    else:
        print(f"No Price Data Found.")
        
    stock_data = stock_data.with_columns([(pl.col(stock_data.columns[1]) / pl.col(stock_data.columns[1]).shift(1) - 1).alias(f"Diff_{stock_ticker}")])
    stock_data = stock_data.select(pl.all().slice(1))
    stock_data = stock_data.with_columns(stock_data[f"Date_{stock_ticker}"].dt.date().alias(f"Date_{stock_ticker}"))

    # Check if the # of rows matches the averaged stocks' number of rows
    if (averaged_stocks.height != stock_data.height):
        print("Entering the loop!")
        stock_data = interpolate(averaged_stocks, stock_data, stock_ticker)

    # If the stock contains an invalid character, have it replaced with a different one - this is only for the file name
    invalids = ["=", "&", "%", "#", "@"]
    stock_ticker_mod = stock_ticker
    for symbol in invalids:
            stock_ticker_mod = stock_ticker_mod.replace(symbol, "_")

    print(f"stock ticker mod: {stock_ticker_mod}")

    # Seeing if the concat  and average files exist first, and deletes the existing one
    file_existence_check(f"{script_dir}\Data\{stock_ticker_mod}_returns_data.csv")

    # Exporting the new .csv files
    export_values_to_csv(f'{stock_ticker_mod}_returns_data.csv', stock_data)

    # Returning the oil data with regular returns
    return stock_data

# Checks the stationarity of a particular set of stock averages
def check_stationarity_general(dataset, stock_ticker_set):
    adf = adfuller(dataset[f"Diff_{stock_ticker_set}"])
    print(f"P-value: {adf[1]}")

    # Confirming stationarity or non stationarity
    if adf[1] < 0.05:
        print("Return values ARE stationary")
        return True
    else:
        print("Return values are NOT stationary.")
        return False

# As of 11/16/2025, the CL=F data contains 2 less data points than the stocks data, so we need to generate an imterpolator to find the spots missing and add them
def interpolate(averaged_stocks, specific_stock, stock_ticker):
    for i in range(averaged_stocks.height):
        if (str(averaged_stocks[i,0]) != str(specific_stock[i,0])):
            # Add an extra row on the specific stock column at the point where the date begins to mismatch
            print(f"Mismatch at the following: Averaged stocks: {averaged_stocks[i,0]} & Specific stock: {specific_stock[i,0]}")
            print(f"Interpolating to get the specific stock date results for {averaged_stocks[i,0]}")

            # Manually slicing the dataframe
            everything_above = specific_stock.slice(0,i)
            everything_below = specific_stock.slice(i)
            price_at_point = np.mean(np.array([specific_stock[i-1,1],specific_stock[i,1]]))
            return_at_point = np.mean(np.array([specific_stock[i-1,2],specific_stock[i,2]]))
            avg_stock_point = datetime.strptime(averaged_stocks[i,0], "%Y-%m-%d").date()
            new_row_data = {f'Date_{stock_ticker}': [avg_stock_point], f'Close_{stock_ticker}': [price_at_point], f'Diff_{stock_ticker}': [return_at_point]}
            new_row = pl.DataFrame(new_row_data)

            # Combining everything back together with newly interpolated (really just averaged) values
            specific_stock = pl.concat([everything_above, new_row, everything_below])

        else:
            continue

    return specific_stock