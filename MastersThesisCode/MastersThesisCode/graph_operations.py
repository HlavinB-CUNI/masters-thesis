import matplotlib.pyplot as plt
import pandas as pd
from math import sqrt
from plotly import data


def plot_prices(dataframe):
    dataframe = dataframe.to_pandas()
    prices_in_question = dataframe.columns[0].split("_",1)[1]
    
    if len(dataframe.columns) > 2:
        plt.plot(dataframe.iloc[:,0], dataframe.iloc[:,1], color = "blue")
        plt.title(f"Plot of Date vs. Price for {prices_in_question}")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.xticks([125, 377, 629, 881, 1133, 1384, 1635, 1887, 2140, 2392, 2643, 2893], 
                        [dataframe.iloc[126, 0], dataframe.iloc[377, 0], dataframe.iloc[629, 0], 
                         dataframe.iloc[881, 0], dataframe.iloc[1133, 0], dataframe.iloc[1384, 0], 
                         dataframe.iloc[1635, 0], dataframe.iloc[1887, 0], dataframe.iloc[2140, 0], 
                         dataframe.iloc[2392, 0], dataframe.iloc[2643, 0], dataframe.iloc[2893, 0]], rotation=40)
        plt.show()
    else:
        print("Dataframe appears to lack any price data. Skipping plot of prices.")
        pass

def plot_returns(dataframe):
    dataframe = dataframe.to_pandas()
    returns_in_question = dataframe.columns[1].split("_",1)[1]

    plt.plot(dataframe.iloc[:,0], dataframe.iloc[:,len(dataframe.columns) - 1], color = "green")
    plt.title(f"Plot of Date vs. Returns for Oil Futures")
    plt.xlabel("Date")
    plt.ylabel("Returns")
    plt.xticks([125, 377, 629, 881, 1133, 1384, 1635, 1887, 2140, 2392, 2643, 2893], 
                        [dataframe.iloc[126, 0], dataframe.iloc[377, 0], dataframe.iloc[629, 0], 
                         dataframe.iloc[881, 0], dataframe.iloc[1133, 0], dataframe.iloc[1384, 0], 
                         dataframe.iloc[1635, 0], dataframe.iloc[1887, 0], dataframe.iloc[2140, 0], 
                         dataframe.iloc[2392, 0], dataframe.iloc[2643, 0], dataframe.iloc[2893, 0]], rotation=40)
    plt.axhline(y=0, color='k', linestyle='-', alpha = 0.5, linewidth = 1)
    plt.show()

def plot_abnormal_returns(dataframe):
    dataframe = dataframe.to_pandas()

    for i in range(0,len(dataframe.columns),3):
        plt.plot(dataframe.iloc[:,i], dataframe.iloc[:, i + 1], color = "green")
        plt.suptitle(f"Plot of Date vs. Abnormal Returns for {dataframe.iloc[5, i]} and +/- 5 Days")
        plt.title(f"Event Classification: {dataframe.iloc[5,i + 2]}")

        plt.xlabel("Date")
        plt.xticks(rotation = 60)
        plt.ylabel("Abnormal Returns")

        plt.grid(color='k', linestyle='-', linewidth=1, alpha = 0.15)
        plt.axhline(0, color='k', linewidth = 1, alpha = 1)
        plt.axvline(dataframe.iloc[5, i], color='goldenrod', linewidth = 1, alpha = 1)

        plt.show()

def plot_rolling_volatility(dataframe):
        
        plt.plot(dataframe['_Date'], dataframe['_RollingVol'], color = "blue")
        plt.title("Plot of Date vs. Volatility for Averaged Oil Stocks")

        plt.xlabel("Date")
        plt.ylabel("Volatility")
        plt.xticks([125, 377, 629, 881, 1133, 1384, 1635, 1887, 2140, 2392, 2643, 2893], 
                        [dataframe.iloc[126, 0], dataframe.iloc[377, 0], dataframe.iloc[629, 0], 
                         dataframe.iloc[881, 0], dataframe.iloc[1133, 0], dataframe.iloc[1384, 0], 
                         dataframe.iloc[1635, 0], dataframe.iloc[1887, 0], dataframe.iloc[2140, 0], 
                         dataframe.iloc[2392, 0], dataframe.iloc[2643, 0], dataframe.iloc[2893, 0]], rotation=40)

        plt.axhline(0.02, color='k', linewidth = 1, alpha = .15)
        plt.axhline(0.04, color='k', linewidth = 1, alpha = .15)
        plt.axhline(0.06, color='k', linewidth = 1, alpha = .15)
        plt.axhline(0.08, color='k', linewidth = 1, alpha = .15)
        plt.axhline(0.10, color='k', linewidth = 1, alpha = .15)

        plt.show()

def plot_specific_volatility(dataframe, dates):

    for i in range(len(dataframe)):
        for j in range (len(dates)):
            if dataframe.iloc[i,0] == dates[j, 1]:
                print(f'Match found at: {dates[j, 1]}')

                # Gathering the month of trading days before and month after
                plotting_df = {'date': dataframe.iloc[i-21:i+22,0].to_list(), 
                               'roll_vol': dataframe.iloc[i-21:i+22,2].to_list()}
                plotting_df = pd.DataFrame(data = plotting_df)

                plt.plot(plotting_df['date'], plotting_df['roll_vol'], color = "blue")

                plt.suptitle(f"Plot of Date vs. Volatility for {dates[j, 1]} and +/- One Month of Trading Days ")
                plt.title(f"Event Classification: {dates[j, 2]}")
                
                plt.xlabel("Date")
                plt.xticks(rotation = 60)
                plt.ylabel("Volatility")
                
                plt.grid(color='k', linestyle='-', linewidth=1, alpha = 0.15)
                plt.axhline(0, color='k', linewidth = 1, alpha = 1)
                plt.axvline(plotting_df.iloc[21, 0], color='goldenrod', linewidth = 1, alpha = 1)
                
                plt.show()

def plot_specific_volatility_garch(dataframe, dates):

    dataframe = dataframe.to_pandas()

    for i in range(len(dataframe)):
        for j in range (len(dates)):
            if dataframe.iloc[i,0] == dates[j, 1]:
                print(f'Match found at: {dates[j, 1]}')

                # Gathering the month of trading days before and month after
                plotting_df = {'date': dataframe.iloc[i-21:i+22,0].to_list(), 
                               'roll_vol': dataframe.iloc[i-21:i+22,2].to_list()}
                plotting_df = pd.DataFrame(data = plotting_df)

                plt.plot(plotting_df['date'], plotting_df['roll_vol'], color = "blue")

                plt.suptitle(f"Plot of Date vs. Volatility for {dates[j, 1]} and +/- One Month of Trading Days ")
                plt.title(f"Event Classification: {dates[j, 2]}")
                
                plt.xlabel("Date")
                plt.xticks(rotation = 60)
                plt.ylabel("Volatility")
                
                plt.grid(color='k', linestyle='-', linewidth=1, alpha = 0.15)
                plt.axhline(0, color='k', linewidth = 1, alpha = 1)
                plt.axvline(plotting_df.iloc[21, 0], color='goldenrod', linewidth = 1, alpha = 1)
                
                plt.show()

def plot_garch_prediction(garch_y_vals):

    # Regular Volatility

    garch_y_pandas = garch_y_vals.to_pandas()

    plt.plot(garch_y_pandas['Date'], garch_y_pandas['True_Volatility'], color = "red")
    plt.suptitle(f"Plot of Date vs. GJR-GARCH Volatility Estimations")

    plt.xlabel("Date")
    plt.xticks([125, 377, 629, 881, 1133, 1384, 1635, 1887, 2140, 2392, 2643, 2893], 
                        [garch_y_pandas.iloc[126, 0], garch_y_pandas.iloc[377, 0], garch_y_pandas.iloc[629, 0], 
                         garch_y_pandas.iloc[881, 0], garch_y_pandas.iloc[1133, 0], garch_y_pandas.iloc[1384, 0], 
                         garch_y_pandas.iloc[1635, 0], garch_y_pandas.iloc[1887, 0], garch_y_pandas.iloc[2140, 0], 
                         garch_y_pandas.iloc[2392, 0], garch_y_pandas.iloc[2643, 0], garch_y_pandas.iloc[2893, 0]], rotation = 40)
    plt.ylabel("Volatility")

    plt.show()

    # Annualized Volatility
    
    garch_y_pandas2 = garch_y_pandas
    garch_y_pandas2['True_Volatility'] = garch_y_pandas2['True_Volatility']*sqrt(252)

    plt.plot(garch_y_pandas2['Date'], garch_y_pandas2['True_Volatility'], color = "red")
    plt.suptitle(f"Plot of Date vs. GJR-GARCH Volatility Estimations")

    plt.xlabel("Date")
    plt.xticks([125, 377, 629, 881, 1133, 1384, 1635, 1887, 2140, 2392, 2643, 2893], 
                        [garch_y_pandas.iloc[126, 0], garch_y_pandas.iloc[377, 0], garch_y_pandas.iloc[629, 0], 
                         garch_y_pandas.iloc[881, 0], garch_y_pandas.iloc[1133, 0], garch_y_pandas.iloc[1384, 0], 
                         garch_y_pandas.iloc[1635, 0], garch_y_pandas.iloc[1887, 0], garch_y_pandas.iloc[2140, 0], 
                         garch_y_pandas.iloc[2392, 0], garch_y_pandas.iloc[2643, 0], garch_y_pandas.iloc[2893, 0]], rotation = 40)
    plt.ylabel("Volatility")

    plt.show()

def plot_combined_prediction(garch_y_vals, roll_vol):

    garch_y_vals = garch_y_vals.to_pandas()

    plt.plot(garch_y_vals['Date'], garch_y_vals['True_Volatility'], color = "red")
    plt.plot(garch_y_vals['Date'], roll_vol['_RollingVol'], color = "blue")
    plt.plot()
    plt.suptitle(f"Plot of Date vs. GJR-GARCH Volatility Estimations")
    plt.legend(['GJR-GARCH Estimate', 'Rolling Window Estimate'], loc = "upper left") 
    
    plt.xlabel("Date")
    plt.xticks([125, 377, 629, 881, 1133, 1384, 1635, 1887, 2140, 2392, 2643, 2893], 
                        [garch_y_vals.iloc[126, 0], garch_y_vals.iloc[377, 0], garch_y_vals.iloc[629, 0], 
                         garch_y_vals.iloc[881, 0], garch_y_vals.iloc[1133, 0], garch_y_vals.iloc[1384, 0], 
                         garch_y_vals.iloc[1635, 0], garch_y_vals.iloc[1887, 0], garch_y_vals.iloc[2140, 0], 
                         garch_y_vals.iloc[2392, 0], garch_y_vals.iloc[2643, 0], garch_y_vals.iloc[2893, 0]], rotation = 40)
    plt.ylabel("Volatility")
    
    plt.show()
