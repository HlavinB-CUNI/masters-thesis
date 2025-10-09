import csv
import numpy as np
import os
import polars as pl
import yfinance as yahoo

def acquire_stock_data(path):

    with open(path, 'r', newline='', encoding = 'utf-8-sig') as tickers:
        csvreader = csv.reader(tickers)

        # Read all rows (tickers) into a list
        rows = list(csvreader)
        
        # Making a polars dataframe of the stocks for show
        rows_polar = pl.DataFrame(rows)
        rows_polar = rows_polar.transpose(include_header=False, column_names=['oil_stocks'])
        stocks = rows_polar['oil_stocks'].to_list()

        # Establishing the dataframe for the stock data
        stock_data = {}

        # Loop to input each individual stock into the list
        for i in stocks:
            # July 1st, 2012 was a Sunday, so the first return will be on July 2nd, and July 1, 2024 was a Monday, so it will be included
            yahoo_df = yahoo.download(i, start = "2012-06-29", end = "2024-07-02", progress = False, auto_adjust = True)
            yahoo_df = yahoo_df.reset_index()
            if yahoo_df.empty == False:
                stock_data[i] = pl.from_pandas(yahoo_df)
            else:
                print(f"Skipping {i}.")
            
        # Converting stock_data to a list
        stock_data = list(stock_data.values())

        # Establishing a new list for specifically adjusted closing returns
        stock_close_data = {}

        # We know that the 12 years of data has 3017 + 2 days, so any stock with less than that amount of rows gets disqualified
        for j in range(len(stock_data)):
            if stock_data[j].select(pl.count()).item() == 3019:
                # Making sure only the close price is included
                stock_close_data[j] = stock_data[j].select(pl.selectors.by_index([0,1]))

                # Adding column for transformed log returns
                stock_close_data[j] = stock_close_data[j].with_columns([(pl.selectors.by_index([1]).log().diff()).alias("log_close_returns")])

                # Removing the excess NA row at the beginning
                stock_close_data[j] = stock_close_data[j].select(pl.all().slice(1))

        stock_close_data = list(stock_close_data.values())

        # Adding column for transformed log returns


        # Printing output to confirm results
        print(stock_close_data)



