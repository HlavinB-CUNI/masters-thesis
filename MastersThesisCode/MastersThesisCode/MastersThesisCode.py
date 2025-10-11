# Final Project for Bryan Hlavin's Master's Thesis
# Topic: Do Russian Aggressions Significnatly Impact US Oil Stocks?
# Made by Bryan Hlavin - Supervisor: Prof. Evzen Kocenda

import os

from acquire_stock_data_func import acquire_stock_data, check_stationarity_stocks
from acquire_general_data_func import acquire_general_data, check_stationarity_general

# Asking the user what they specifically want to see or calculate
print('Please select a number for what you would like to see.')

user_request = int(input("Enter valid number: "))

# Get absolute path of *this* script
script_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(script_dir, 'Data', 'tickers_only.csv')

def switch(user_request):
    if user_request == 1:
        print('Dataframe Generation of all Oil and Gas Stocks')
        stocks = acquire_stock_data(path)
        check_stationarity_stocks(stocks)
    
    elif user_request == 2:
        print('Dataframe Generation of Crude Oil Price')
        oil = acquire_general_data("CL=F")
        check_stationarity_general(oil, "CL=F")

    elif user_request == 3:
        print('Dataframe Generation of SP500 Price')
        SP500 = acquire_general_data("^SPX")
        check_stationarity_general(SP500, "^SPX")

    elif user_request == 4:
        print('Generalized Graphing Operations')


    elif user_request == 5:
        print('ARIMA Calculations')


    elif user_request == 6: 
        print('Abnormal Returns Calculations')


    elif user_request == 7:
        print('Rolling Volatility Calculations')


    elif user_request == 8:
        print('Graphing of ARIMA')


    elif user_request == 9:
        print('Graphing of Abnormal Stock Returns')


    elif user_request == 10:
        print('Graphing of Rolling Volatility')


    else:
        print("You have not imputted a valid number. Please try again. ")
        user_request = input("Enter valid number: ")
        user_request = int(user_request)

switch(user_request)

# Option 1: Collection of all Oil and Gas Stocks which are part of this paper

# Option 2: Calculations for ARIMA

# Option 3: Calculations for Abnormal Returns

# Option 4: Rolling Volitility Calculations

# Option 5: Graphing of ARIMA 

# Option 6: Graphing of Abnormal Stock Returns

# Option 7: Graphing of Rolling Volatility
