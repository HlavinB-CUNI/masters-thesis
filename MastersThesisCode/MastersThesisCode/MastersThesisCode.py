# Final Project for Bryan Hlavin's Master's Thesis
# Topic: Do Russian Aggressions Significnatly Impact US Oil Stocks?
# Made by Bryan Hlavin - Supervisor: Prof. Evzen Kocenda

# Importing everything necessary
import os
import sys
from graph_operations import plot_prices, plot_returns, plot_abnormal_returns, plot_specific_volatility
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
extended_dataframe = file_to_dataframe_check(os.path.join(script_dir, 'Data', 'rescaled_dataframe_all_vars.csv'))
rolling_volatility_calculated = file_to_dataframe_check(os.path.join(script_dir, 'Data', 'rolling_volatility_calcs.csv'))
print("-------------------------------------------------")


def switch(user_request, stocks, oil, SP500, dummy_vars, sig_dates, ab_rets, cum_ab_rets, extended_dataframe):

    # Combining every variable into one dataframe for simplicity (if obtained)
    all_variables = dummy_vars
    all_variables = all_variables.with_columns(stocks[:,1])
    all_variables = all_variables.with_columns(SP500[:,2])
    all_variables = all_variables.with_columns(oil[:,2])
    
    if user_request == 1:
        print('Dataframe Generation of all Oil and Gas Stocks Returns')
        stocks = acquire_stock_data(path)
        check_stationarity_stocks(stocks)
    
    elif user_request == 2:
        print('Dataframe Generation of Crude Oil Prices & Returns')
        oil = acquire_general_data("CL=F", stocks)
        check_stationarity_general(oil, "CL=F")

    elif user_request == 3:
        print('Dataframe Generation of SP500 Price')
        SP500 = acquire_general_data("^SPX", stocks)
        check_stationarity_general(SP500, "^SPX")

    elif user_request == 4:
        print('Graphing of Stocks & Returns')
        
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
        print('ARMA-GARCH Calculations and Graphing')

        # fitting all the values 
        plot_acf_pacf(stocks, 'Averaged Stocks')

        # Fitting the ARMA models individually for each of the returns sets, choosing ARIMA order
        stocks_fit = arma_fit(stocks, 'Averaged Stocks')

        # ADF tests done already, and stationarity has been confirmed

        # Moving onto including the exogenous variables (this problably isn't needed)
        # arimax_stocks_fit = arimax_fit(all_variables, stocks_fit)

        # Actually doing the ARMA-GJR-GARCH modeling, passing in the entire dataframe, and averaged stocks ARMA values
        # This code also generates the entire variables file to be a holistic dataframe for all variables
        print(f'Performing GJR-GARCH Test with the stocks fitted to ARMA({stocks_fit[0]},{stocks_fit[1]}).')
        extended_dataframe = garch_test(all_variables, stocks_fit[0], stocks_fit[1]) # return variable is a modified dataframe of all the variables, with columns with returns*100

        # Graphing the garch results


    elif user_request == 7:
        print('Rolling Volatility Calculations')

        # Calculating the rolling volatility under a month window time frame for the averaged oil stock returns
        rolling_volatility_calculated = compute_rolling_volatility(stocks, 21) # plotting included in this function for the overall volatility

        # Volatility plots (2 month time period of trading days) for specific events
        plot_specific_volatility(rolling_volatility_calculated, sig_dates)

    return stocks, oil, SP500, ab_rets, cum_ab_rets, all_variables, extended_dataframe, rolling_volatility_calculated

#########################################################################################################################
# Asking the user what they specifically want to see or calculate
print('Please select the corresponding number for what action you would like to perform.')
print('Options:' +
     '\n' + '1) Dataframe Generation of all Oil and Gas Stocks Returns' +
     '\n' + '2) Dataframe Generation of Crude Oil Prices & Returns'
     '\n' + '3) Dataframe Generation of S&P 500 Prices & Returns'
     '\n' + '4) Graphing of Stocks and Returns'
     '\n' + '5) Abnormal Returns Calculations and Graphing'
     '\n' + '6) ARMA-GJR-GARCH Operations and Graphing'
     '\n' + '7) Rolling Volatility Calculations'
     '\n' + '8) Exit Application')

# Loop if the user wants to do more than one thing while the process is running
loop_program = True
user_request_int = 0
while loop_program == True:

    # Loop to ensure that a valid number is selected, and it will not continue until it is. 
    enter_switch = False
    while enter_switch == False:

        # Asking the user to input a valid number
        user_request = str(input("Enter valid number: "))
        if user_request in ['1','2','3','4','5','6','7']:
            print(f"You have selected number {user_request}.")
            user_request_int = int(user_request)
            enter_switch = True
        elif user_request in ['8']:
            print("Ending process.")
            sys.exit()
        else:
            print("Incorrect input, please input a valid number.")
            enter_switch = False

    # Running the switch statement to start the program
    stocks, oil, SP500, ab_rets, cum_ab_rets, all_variables, extended_dataframe, rolling_volatility_calculated = switch(user_request_int, stocks, oil, SP500, dummy_variables, significant_dates, abnormal_returns_complete, cumulative_abnormal_returns_complete, extended_dataframe)
