import polars as pl
import polars_ols as pols
import os
import math
import scipy.stats as st
from file_operations import file_existence_check, export_values_to_csv

# Calculates the abnormal returns values and standardizes them for an 11 day period (5 before, 1 on, 5 after)
def abnormal_returns_calc(stocks, SP500, dates):
    # Establishing list of dataframes
    abnormal_returns = []
    date_column_counter = 0

    # OLS Market Model Establishment
    df_stocks_sp500 = pl.concat([stocks, SP500], how = "horizontal")
    df_stocks_sp500 = df_stocks_sp500.drop(['Date_^SPX', 'Close_^SPX'])

    stocks_ols = (df_stocks_sp500.select(
    pl.col("_Mean-Oil-Stocks").least_squares.ols(pl.col("Diff_^SPX"), mode="statistics", add_intercept=True))
    .unnest("statistics").explode(["feature_names", "coefficients", "standard_errors", "t_values", "p_values"]))

    # Loop to find each specific date string in the larger dataframes
    for i in range(len(stocks)):
        for j in range (len(dates)):
            if stocks[i,0] == dates[j, 1]:

                # Temporary holding place before converting into polars dataframe
                temp_rets = []

                # Appending everything properly
                temp_rets.append({f"Date_{date_column_counter}": stocks[i-5,0], 
                                  f"AbReturn_{date_column_counter}": (stocks[i-5,1] - (stocks_ols[1, 'coefficients'] + stocks_ols[0, 'coefficients']*SP500[i-5,2])), 
                                  f"Event_Type_{date_column_counter}": dates[j,2]})
                temp_rets.append({f"Date_{date_column_counter}": stocks[i-4,0], 
                                  f"AbReturn_{date_column_counter}": (stocks[i-4,1] - (stocks_ols[1, 'coefficients'] + stocks_ols[0, 'coefficients']*SP500[i-4,2])), 
                                  f"Event_Type_{date_column_counter}": dates[j,2]})
                temp_rets.append({f"Date_{date_column_counter}": stocks[i-3,0], 
                                  f"AbReturn_{date_column_counter}": (stocks[i-3,1] - (stocks_ols[1, 'coefficients'] + stocks_ols[0, 'coefficients']*SP500[i-3,2])), 
                                  f"Event_Type_{date_column_counter}": dates[j,2]})
                temp_rets.append({f"Date_{date_column_counter}": stocks[i-2,0], 
                                  f"AbReturn_{date_column_counter}": (stocks[i-2,1] - (stocks_ols[1, 'coefficients'] + stocks_ols[0, 'coefficients']*SP500[i-2,2])), 
                                  f"Event_Type_{date_column_counter}": dates[j,2]})
                temp_rets.append({f"Date_{date_column_counter}": stocks[i-1,0], 
                                  f"AbReturn_{date_column_counter}": (stocks[i-1,1] - (stocks_ols[1, 'coefficients'] + stocks_ols[0, 'coefficients']*SP500[i-1,2])), 
                                  f"Event_Type_{date_column_counter}": dates[j,2]})
                temp_rets.append({f"Date_{date_column_counter}": stocks[i,0],   
                                  f"AbReturn_{date_column_counter}": (stocks[i,1] - (stocks_ols[1, 'coefficients'] + stocks_ols[0, 'coefficients']*SP500[i,2])),   
                                  f"Event_Type_{date_column_counter}": dates[j,2]})
                temp_rets.append({f"Date_{date_column_counter}": stocks[i+1,0], 
                                  f"AbReturn_{date_column_counter}": (stocks[i+1,1] - (stocks_ols[1, 'coefficients'] + stocks_ols[0, 'coefficients']*SP500[i+1,2])), 
                                  f"Event_Type_{date_column_counter}": dates[j,2]})
                temp_rets.append({f"Date_{date_column_counter}": stocks[i+2,0], 
                                  f"AbReturn_{date_column_counter}": (stocks[i+2,1] - (stocks_ols[1, 'coefficients'] + stocks_ols[0, 'coefficients']*SP500[i+2,2])), 
                                  f"Event_Type_{date_column_counter}": dates[j,2]})
                temp_rets.append({f"Date_{date_column_counter}": stocks[i+3,0], 
                                  f"AbReturn_{date_column_counter}": (stocks[i+3,1] - (stocks_ols[1, 'coefficients'] + stocks_ols[0, 'coefficients']*SP500[i+3,2])), 
                                  f"Event_Type_{date_column_counter}": dates[j,2]})
                temp_rets.append({f"Date_{date_column_counter}": stocks[i+4,0], 
                                  f"AbReturn_{date_column_counter}": (stocks[i+4,1] - (stocks_ols[1, 'coefficients'] + stocks_ols[0, 'coefficients']*SP500[i+4,2])), 
                                  f"Event_Type_{date_column_counter}": dates[j,2]})
                temp_rets.append({f"Date_{date_column_counter}": stocks[i+5,0], 
                                  f"AbReturn_{date_column_counter}": (stocks[i+5,1] - (stocks_ols[1, 'coefficients'] + stocks_ols[0, 'coefficients']*SP500[i+5,2])), 
                                  f"Event_Type_{date_column_counter}": dates[j,2]})

                date_column_counter = date_column_counter + 1

                # Converting to polars dataframe and moving into the abnormal_returns list
                temp_rets = pl.DataFrame(temp_rets)
                abnormal_returns.append(temp_rets) 

    # Combinging all dataframes together into one giant one to make things simple
    abnormal_returns_complete = pl.concat(abnormal_returns, how = "horizontal")

    # Sum of all abnormal returns calculations (calculations sum for a specific date in one dataframe)
    cumulative_abnormal_returns_complete = abnormal_returns_complete.sum()

    for k in range(len(dates)):
            cumulative_abnormal_returns_complete = cumulative_abnormal_returns_complete.drop([f'Date_{k}', f'Event_Type_{k}'])
    # Return dataframe of  & dataframe of sum of abnormal returns calculations)

    script_dir = os.path.dirname(os.path.abspath(__file__))

    file_existence_check(f"{script_dir}\Data\abnormal_rets_complete.csv")
    file_existence_check(f"{script_dir}\Data\cumu_abnormal_rets_complete.csv") 

    # Exporting the new .csv files
    export_values_to_csv('abnormal_rets_complete.csv', abnormal_returns_complete)
    export_values_to_csv('cumu_abnormal_rets_complete.csv', cumulative_abnormal_returns_complete)

    print(abnormal_returns_complete)
    print(cumulative_abnormal_returns_complete)

    return abnormal_returns_complete, cumulative_abnormal_returns_complete


def generalized_sign_test(ab_rets, stocks):
    w = 0
    N = 11
    script_dir = os.path.dirname(os.path.abspath(__file__))

    w_variables = []
    z_values = []
    date_event = []
    type_event = []
    p_values = []
    significant_status = []

    # calculating the quantity of positive returns in each set of abnormal returns
    for l in range(ab_rets.width):
        w = 0
        if l in [1,4,7,10,13,16,19,22,25,28,31,34,37,40,43,46,49,52,55,58,61]:
            for m in range(ab_rets.height):
                if ab_rets[m,l] >= 0:
                    w = w + 1
            w_variables.append(w)
            date_event.append(ab_rets[5,l-1]) # getting the position of the event date 
            type_event.append(ab_rets[0,l+1]) # getting the position of the event name

    # will be calculated as percentage of positives throughout every observation window combined (this is r_hat)
    pos_pct = sum(w_variables) / ((ab_rets.width / 3)*11)

    # adding all the percentage and z-value calculations
    for n in range(len(w_variables)):
        z_values.append((w_variables[n] - (N*pos_pct)) / math.sqrt(N*pos_pct*(1-pos_pct)))

        # test for significance with the p-value
        p_values.append(2*st.norm.sf(abs(z_values[n])))
        if (p_values[n] > 0.05): # reminder that this alpha level can be changed only internally
            significant_status.append('NOT SIGNIFICANT')
        else:
            significant_status.append('SIGNIFICANT')

    date_event_df = pl.DataFrame(date_event).rename({"column_0":"Date"})
    type_event_df = pl.DataFrame(type_event).rename({"column_0":"Event_Type"})
    w_variables_df = pl.DataFrame(w_variables).rename({"column_0":"w"})
    z_values_df = pl.DataFrame(z_values).rename({"column_0":"z_value"})
    p_values_df = pl.DataFrame(p_values).rename({"column_0":"p_value"})
    significant_status_df = pl.DataFrame(significant_status).rename({"column_0":"Test_For_Significance"})

    # Combining into own dataframe
    z_values_df = pl.concat([date_event_df, w_variables_df, z_values_df, p_values_df, significant_status_df, type_event_df], how = "horizontal")

    # Output to file
    file_existence_check(f"{script_dir}\Data\z_values_df.csv")

    # Exporting the new .csv files
    export_values_to_csv('z_values_df.csv', z_values_df)
    
    print(z_values_df)

    return