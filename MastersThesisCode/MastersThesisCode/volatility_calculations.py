from graph_operations import plot_rolling_volatility
from file_operations import file_existence_check, export_values_to_csv
import polars as pl
import os

# Ultimately, these results were not used in the final draft of the thesis paper. However, the code will remain here just in case it is needed in the future.
def compute_rolling_volatility(stock_rets, days):

    # Need to convert to pandas for calculations
    df = stock_rets.to_pandas()

    # Adding in the rolling volatility for a month's worth of trading days
    df['_RollingVol'] = df['_Mean-Oil-Stocks'].rolling(days).std()

    # Plotting the rolling volatility
    plot_rolling_volatility(df)

    # Establishing the directory path for all files for this project
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Exporting the new scaled data to .csv 
    file_existence_check(f"{script_dir}\Data\rolling_volatility_calcs.csv")
    export_values_to_csv('rolling_volatility_calcs.csv', pl.from_pandas(df))
    
    return df
