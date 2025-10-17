import polars as pl


# Calculates the abnormal returns values and standardizes them for an 11 day period (5 before, 1 on, 5 after)
def abnormal_returns_calc(stocks, SP500, dates):
    # Establishing list of dataframes
    abnormal_returns = []

    # Establishing dataframe for sums
    #df_sum_abnormal_returns = pl.DataFrame()

    # Loop to find each specific date string in the larger dataframes
    for i in range(len(stocks)):
        for j in range (len(dates)):
            if stocks[i,0] == dates[j, 1]:
                print(f'Match found! at {dates[j,1]}')

                # Temporary holding place before converting into polars dataframe
                temp_rets = []

                # Appending everything properly
                temp_rets.append({"Date": stocks[i-5,0], "Return": stocks[i-5,1], "Event_Type": dates[j,2]})
                temp_rets.append({"Date": stocks[i-4,0], "Return": stocks[i-4,1], "Event_Type": dates[j,2]})
                temp_rets.append({"Date": stocks[i-3,0], "Return": stocks[i-3,1], "Event_Type": dates[j,2]})
                temp_rets.append({"Date": stocks[i-2,0], "Return": stocks[i-2,1], "Event_Type": dates[j,2]})
                temp_rets.append({"Date": stocks[i-1,0], "Return": stocks[i-1,1], "Event_Type": dates[j,2]})
                temp_rets.append({"Date": stocks[i,0], "Return": stocks[i,1], "Event_Type": dates[j,2]})
                temp_rets.append({"Date": stocks[i+1,0], "Return": stocks[i+1,1], "Event_Type": dates[j,2]})
                temp_rets.append({"Date": stocks[i+2,0], "Return": stocks[i+2,1], "Event_Type": dates[j,2]})
                temp_rets.append({"Date": stocks[i+3,0], "Return": stocks[i+3,1], "Event_Type": dates[j,2]})
                temp_rets.append({"Date": stocks[i+4,0], "Return": stocks[i+4,1], "Event_Type": dates[j,2]})
                temp_rets.append({"Date": stocks[i+5,0], "Return": stocks[i+5,1], "Event_Type": dates[j,2]})

                # Converting to polars dataframe and moving into the abnormal_returns list
                temp_rets = pl.DataFrame(temp_rets)
                abnormal_returns.append(temp_rets)   
    print(f'Abnormal returns: {abnormal_returns}') # concatenate this!! and make sure that this is 

        # If there is a match, then (loop calculate the daily returns for the specified time period

        # Standardize the returns (might remove this later)

        # (average abnormal returns can be skipped, because the stock returns are already averaged)
        # Make a list of polars dataframes to store each set of calculations for every date

        # Sum of all abnormal returns calculations (calculations sum for a specific date in one dataframe)

    # Return dataframe of  & dataframe of sum of abnormal returns calculations

