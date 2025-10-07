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

        for i in stocks:
            yahoo_df = yahoo.download(i, start = "2012-07-01", end = "2024-07-01", progress = False, auto_adjust = True)
            yahoo_df = yahoo_df.reset_index()
            if yahoo_df.empty == False:
                stock_data[i] = pl.from_pandas(yahoo_df)
            else:
                print(f"Skipping {i}.")
            
        # We know that the 12 years of data has 3017 days, so any stock with less than that amount of rows gets disqualified
        #for j in stock_data:
        # Converting stock_data to a list
        stock_data = list(stock_data.values())
        print(stock_data)
        # Making sure only the close price is included
        #stock_close_data = {}
        print(stock_data[1])
        #for i in range(len(stock_data)):
        #    stock_close_data[i] = stock_data[i].select(pl.selectors.by_index([0,1]))

        # Gives the total number of valid stocks for the time period
        #print(len(stock_close_data))
        #print(stock_close_data)



