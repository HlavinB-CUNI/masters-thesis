import csv
import os

def acquire_stock_data():
    path = os.path.expanduser('/Data/tickers_only.csv')  # fix path with ~
    with open(path, 'r', newline='') as tickers:
        csvreader = csv.reader(tickers)

        # Read all rows into a list
        rows = list(csvreader)

        # Print row count
        print(f"Total no. of rows: {len(rows)}")

        # Print each row
        for row in rows:
            print(row)

