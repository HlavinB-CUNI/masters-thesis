# Final Project for Bryan Hlavin's Master's Thesis
# Topic: Do Russian Aggressions Significnatly Impact US Oil Stocks?
# Made by Bryan Hlavin - Supervisor: Prof. Evzen Kocenda

import os
import polars as pl
from graph_operations import plot_prices, plot_returns, plot_abnormal_returns
from file_operations import file_to_dataframe_check
from acquire_stock_data_func import acquire_stock_data, check_stationarity_stocks
from acquire_general_data_func import acquire_general_data, check_stationarity_general
from abnormal_returns_calculations import abnormal_returns_calc, generalized_sign_test
from arima_operations import arma_fit, plot_acf_pacf, garch_test
from volatility_calculations import compute_rolling_volatility

# Get absolute path of *this* script
script_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(script_dir, 'Data', 'tickers_only.csv')

# Loading in dataframes for the files necessary to do this analysis (if they exist)
stocks = file_to_dataframe_check(os.path.join(script_dir, 'Data', 'stock_data_average.csv'))
oil = file_to_dataframe_check(os.path.join(script_dir, 'Data', 'CL_F_returns_data.csv')) 
SP500 = file_to_dataframe_check(os.path.join(script_dir, 'Data', '^SPX_returns_data.csv'))
dummy_variables = file_to_dataframe_check(os.path.join(script_dir, 'Data', 'dummy_variables.csv'))
significant_dates = file_to_dataframe_check(os.path.join(script_dir, 'Data', 'dummy_events.csv'))
abnormal_returns_complete = file_to_dataframe_check(os.path.join(script_dir, 'Data', 'abnormal_rets_complete.csv'))
cumulative_abnormal_returns_complete = file_to_dataframe_check(os.path.join(script_dir, 'Data', 'cumu_abnormal_rets_complete.csv'))
all_variables = file_to_dataframe_check(os.path.join(script_dir, 'Data', 'rescaled_dataframe_all_vars.csv'))
print("-------------------------------------------------")

# Asking the user what they specifically want to see or calculate
print('Please select a number for what action you would like to perform.')
user_request = int(input("Enter valid number: "))

def switch(user_request, stocks, oil, SP500, dummy_vars, sig_dates, ab_rets, cum_ab_rets, all_variables):
    if user_request == 1:
        print('Dataframe Generation of all Oil and Gas Stocks')
        stocks = acquire_stock_data(path)
        check_stationarity_stocks(stocks)
    
    elif user_request == 2:
        print('Dataframe Generation of Crude Oil Price')
        oil = acquire_general_data("CL=F", stocks)
        check_stationarity_general(oil, "CL=F")

    elif user_request == 3:
        print('Dataframe Generation of SP500 Price')
        SP500 = acquire_general_data("^SPX", stocks)
        check_stationarity_general(SP500, "^SPX")

    elif user_request == 4:
        print('Generalized Graphing Operations')
        
        # Options for stock graph and returns graph
        print('Please select a number for what action you would like to perform.')
        print("1.) Oil 2.) SP500, 3.) Avg. US Oil Stocks")
        user_request_plots = int(input("Enter valid number: "))
        if user_request_plots == 1:
            plot_prices(oil)
            plot_returns(oil)
        elif user_request_plots == 2:
            plot_prices(SP500)
            plot_returns(SP500)
        elif user_request_plots == 3:
            plot_prices(stocks)
            plot_returns(stocks)

    elif user_request == 5:
        print('Abnormal Returns Calculations')
        # SP500 is the benchmark
        # 11 day horizon (5 before, 1 on, 5 after)
        print('Would you like to calculate the abnormal returns, and export to files? (y/n)')
        user_request_retscalcs = input(f"Enter answer: ")
        if user_request_retscalcs.lower() == "yes" or user_request_retscalcs.lower() == "y":
            ab_rets, cum_ab_rets = abnormal_returns_calc(stocks, SP500, significant_dates)
        elif user_request_retscalcs.lower() == "no" or user_request_retscalcs.lower() == "n":
            pass

        # Options for stock graph and returns graph
        print('Would you like to graph the average returns? (y/n)')
        user_request_plots = input(f"Enter answer: ")
        if user_request_plots.lower() == "yes" or user_request_plots.lower() == "y":
            plot_abnormal_returns(ab_rets)
        elif user_request_plots.lower() == "no" or user_request_plots.lower() == "n":
            pass

        # Generalized sign test for significance
        print('Would you like to perform a Generalized Sign test for significance? (y/n)')
        user_request_tests = input(f"Enter answer: ")
        if user_request_tests.lower() == "yes" or user_request_tests.lower() == "y":
            generalized_sign_test(ab_rets, stocks)
        elif user_request_tests.lower() == "no" or user_request_tests.lower() == "n":
            pass

    elif user_request == 6:
        print('ARMA-GARCH Calculations')

        # Combining every variable into one dataframe for simplicity
        all_variables = dummy_vars
        all_variables = all_variables.with_columns(stocks[:,1])
        all_variables = all_variables.with_columns(SP500[:,2])
        all_variables = all_variables.with_columns(oil[:,2])

        # fitting all the values 
        plot_acf_pacf(stocks, 'Averaged Stocks')

        # Fitting the ARMA models individually for each of the returns sets, choosing ARIMA order
        stocks_fit = arma_fit(stocks, 'Averaged Stocks')

        # ADF tests done already, and stationarity has been confirmed

        # Moving onto including the exogenous variables (this problably isn't needed)
        # arimax_stocks_fit = arimax_fit(all_variables, stocks_fit)

        # Actually doing the ARMA-GJR-GARCH modeling, passing in the entire dataframe, and averaged stocks ARMA values
        print(f'Performing GJR-GARCH Test with the stocks fitted to ARMA({stocks_fit[0]},{stocks_fit[1]}).')
        extended_dataframe = garch_test(all_variables, stocks_fit[0], stocks_fit[1]) # return variable is a modified dataframe of all the variables, with columns with returns*100

    elif user_request == 7:
        print('Rolling Volatility Calculations')

        # Calculating the rolling volatility under a month window time frame for the averaged oil stock returns
        compute_rolling_volatility(stocks, 22)

    elif user_request == 8:
        print('Graphing of ARIMA')


    elif user_request == 9:
        print('Graphing of Rolling Volatility')


    else:
        print("You have not imputted a valid number. Please try again. ")
        user_request = input("Enter valid number: ")
        user_request = int(user_request)

    return stocks, oil, SP500, ab_rets, cum_ab_rets, all_variables

switch(user_request, stocks, oil, SP500, dummy_variables, significant_dates, abnormal_returns_complete, cumulative_abnormal_returns_complete, all_variables)
