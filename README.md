# masters-thesis
Code for the master's thesis topic of “Do Russian Aggressions Significantly Impact US Oil Stocks?” at Charles University, Faculty of Social Sciences, Institute of Economic Studies

## Code
The code is structured in a way that functions can be accessed based on each segment of the project (abnormal returns, GJR-GARCH, graphing).
The files used are:

1. MastersThesisCode.py - Starting file to run. Allows the user to select what specifically they need done.
2. file_operations.py - All operations for saving files, generating files, and opening/closing files
3. acquire_general_data_func.py - Functions for acquiring the SP500 and oil futures (+ stationarity checks)
4. acquire_stock_data_func.py - Functions for getting as many oil and gas stocks that meet the criteria for dates traded (+ stationarity checks)
5. abnormal_returns_calculations.py - Contains the abnormal returns formulas from the Mean Model equation, and also the Cowan sign test function.
6. arima_operations.py - Performing the GJR-GARCH analysis from start to finish (includes Ljung-Box testing)
7. volatility_calculations.py - Performs the rolling volatility calculation (not used in thesis paper)
8. graph_operations.py - All operations for visually displaying the results in a variety of manners

## Raw data, variable tables, and calculated results
All .csv files used and generated are located in the Data folder. The raw stock information used in calculations for this thesis are stored here, along with the calculated averages and returns. 
All calculated results from any testing (Cowan Sign Test, GJR-GARCH) done are also located in this folder. 
