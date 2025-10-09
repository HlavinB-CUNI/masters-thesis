import csv
import os
import polars as pl
import yfinance as yahoo

def acquire_stock_data(path):

    with open(path, 'r', newline='', encoding = 'utf-8-sig') as tickers:
        csvreader = csv.reader(tickers)

        # Read all rows (tickers) into a list
        rows = list(csvreader)
        rows2 = [r[0] for r in rows] 
        
        # Making a polars dataframe of the stocks for show
        rows_polar = pl.DataFrame(rows)
        rows_polar = rows_polar.transpose(include_header=False, column_names=['oil_stocks'])
        stocks = rows_polar['oil_stocks'].to_list()

        # Establishing the dataframe for the stock data
        stock_data = {}

        # Loop to input each individual stock into the list
        for i in stocks:
            yahoo_df = yahoo.download(i, start = "2012-07-01", end = "2024-07-01", progress = False, auto_adjust = True)
            yahoo_df = yahoo_df.reset_index()
            if yahoo_df.empty == False:
                stock_data[i] = pl.from_pandas(yahoo_df)
            else:
                print(f"Skipping {i}.")
            
        # Converting stock_data to a list
        stock_data = list(stock_data.values())

        # Establishing a new list for specifically adjusted closing returns
        stock_close_data = {}

        # We know that the 12 years of data has 3017 days, so any stock with less than that amount of rows gets disqualified
        for j in range(len(stock_data)):
            if stock_data[j].select(pl.count()).item() == 3017:
                # Making sure only the close price is included
                stock_close_data[j] = stock_data[j].select(pl.selectors.by_index([0,1]))

        print(stock_close_data)

        # Gives the total number of valid stocks for the time period
        #print(len(stock_close_data))
        #print(stock_close_data)



