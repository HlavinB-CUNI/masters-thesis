import matplotlib.pyplot as plt

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
                         dataframe.iloc[2392, 0], dataframe.iloc[2643, 0], dataframe.iloc[2893, 0]], rotation=60)
        plt.show()
    else:
        print("Dataframe appears to lack any price data. Skipping plot of prices.")
        pass

def plot_returns(dataframe):
    dataframe = dataframe.to_pandas()
    returns_in_question = dataframe.columns[1].split("_",1)[1]

    plt.plot(dataframe.iloc[:,0], dataframe.iloc[:,len(dataframe.columns) - 1], color = "red")
    plt.title(f"Plot of Date vs. Returns for {returns_in_question}")
    plt.xlabel("Date")
    plt.ylabel("Returns")
    plt.xticks([125, 377, 629, 881, 1133, 1384, 1635, 1887, 2140, 2392, 2643, 2893], 
                        [dataframe.iloc[126, 0], dataframe.iloc[377, 0], dataframe.iloc[629, 0], 
                         dataframe.iloc[881, 0], dataframe.iloc[1133, 0], dataframe.iloc[1384, 0], 
                         dataframe.iloc[1635, 0], dataframe.iloc[1887, 0], dataframe.iloc[2140, 0], 
                         dataframe.iloc[2392, 0], dataframe.iloc[2643, 0], dataframe.iloc[2893, 0]], rotation=60)
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