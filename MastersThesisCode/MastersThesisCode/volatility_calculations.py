from graph_operations import plot_rolling_volatility


def compute_rolling_volatility(stock_rets, days):

    # Need to convert to xts
    df = stock_rets.to_pandas()

    # Adding in the rolling volatility for a month's worth of trading days
    df['_RollingVol'] = df['_Mean-Oil-Stocks'].rolling(days).std()

    # Plotting the rolling volatility
    plot_rolling_volatility(df)
    
    return 
