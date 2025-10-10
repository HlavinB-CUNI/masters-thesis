import csv
import os
import polars as pl
import yfinance as yahoo

# Function for if the user wishes to re-acquire fresh data using the list of stocks
def acquire_stock_data(path):

    with open(path, 'r', newline='', encoding = 'utf-8-sig') as tickers:
        csvreader = csv.reader(tickers)

        # Read all rows (tickers) into a list
        rows = list(csvreader)
        
        # Making a polars dataframe of the stocks for show
        rows_polar = pl.DataFrame(rows)
        rows_polar = rows_polar.transpose(include_header=False, column_names=['oil_stocks'])
        stocks = rows_polar['oil_stocks'].to_list()

        # Making a list of the valid stocks
        valid_stocks = list()

        # Establishing the dataframe for the stock data
        stock_data = {}

        # Loop to input each individual stock into the list
        for i in stocks:
            # July 1st, 2012 was a Sunday, so the first return will be on July 2nd, and July 1, 2024 was a Monday, so it will be included
            yahoo_df = yahoo.download(i, start = "2012-06-29", end = "2024-07-02", progress = False, auto_adjust = True)
            yahoo_df = yahoo_df.reset_index()
            if yahoo_df.empty == False:
                stock_data[i] = pl.from_pandas(yahoo_df)
                stock_data[i] = stock_data[i].rename({f"('Date', '')":f"Date_{i}", f"('Close', '{i}')":f"Close_{i}"})

                valid_stocks.append(i)
            else:
                print(f"Skipping {i}.")
            
        # Converting stock_data to a list
        stock_data = list(stock_data.values())

        # Establishing a new list for specifically adjusted closing returns
        stock_close_data = {}

        # We know that the 12 years of data has 3017 + 2 days for data offset, so any stock with less than that amount of rows gets disqualified
        for j in range(len(stock_data)):
            if stock_data[j].select(pl.count()).item() == 3019:
                # Making sure only the close price is included
                stock_close_data[j] = stock_data[j].select(pl.selectors.by_index([0,1]))

                # Adding column for transformed log returns
                stock_close_data[j] = stock_close_data[j].with_columns([(pl.selectors.by_index([1]).log().diff()).alias(f"Log_{stock_close_data[j].columns[1]}")])

                # Removing the excess NA row at the beginning
                stock_close_data[j] = stock_close_data[j].select(pl.all().slice(1))
                
        stock_close_data = list(stock_close_data.values())

        # Printing output to confirm results
        #print(stock_close_data)

        # Setting up concat dataframes
        stock_close_data_concat = stock_close_data[0]
        stock_close_data_concat_log = stock_close_data[0]

        # Looping to concatenate everything
        for k in range(1, len(stock_close_data)):
            stock_close_data_concat = pl.concat([stock_close_data_concat, stock_close_data[k].select(pl.selectors.by_index([1,2]))], how = "horizontal") 

        for l in range(1, len(stock_close_data)):
            stock_close_data_concat_log = pl.concat([stock_close_data_concat_log, stock_close_data[l].select(pl.selectors.by_index([2]))], how = "horizontal") # only log returns at index 2

        # Fixing columns in the concat log dataframe 
        stock_close_data_concat_log = stock_close_data_concat_log.drop(f"Close_{valid_stocks[0]}")

        # Renaming first column to just 'Date' instead of 'Date_' + first stock ticker
        stock_close_data_concat = stock_close_data_concat.rename({f"Date_{valid_stocks[0]}":f"Date"})
        stock_close_data_concat_log = stock_close_data_concat_log.rename({f"Date_{valid_stocks[0]}":f"Date"})

        # Exporting all stocks uniquely to .csv
        script_dir = os.path.dirname(os.path.abspath(__file__))
        path_concat = os.path.join(script_dir, 'Data', 'stock_data_concat.csv')
        stock_close_data_concat.write_csv(path_concat)

        # Setting up averaging dataframe
        stock_close_data_average_log = stock_close_data_concat_log.with_columns(pl.mean_horizontal(pl.exclude("Date")).alias("Average"))
        
        # Loop to remove every other column except the average one
        for m in valid_stocks:
            stock_close_data_average_log = stock_close_data_average_log.drop(pl.exclude(["Date", "Average"]))

        print("Average log.")
        print(stock_close_data_average_log)

        # Exporting mean of all stocks per day as a .csv.
        path_average = os.path.join(script_dir, 'Data', 'stock_data_average.csv')
        stock_close_data_concat_log.write_csv(path_average)





