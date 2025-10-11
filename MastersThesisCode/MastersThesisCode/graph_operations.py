import matplotlib.pyplot as plt
import polars as pl
import numpy as np
import pandas as pd

def plot_prices(dataframe):
    dataframe = dataframe.to_pandas()
    prices_in_question = dataframe.columns[0].split("_",1)[1]

    plt.plot(dataframe.iloc[:,0], dataframe.iloc[:,1], color = "blue")
    plt.title(f"Plot of Date vs. Price for {prices_in_question}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.show()

def plot_returns(dataframe):
    dataframe = dataframe.to_pandas()
    returns_in_question = dataframe.columns[0].split("_",1)[1]

    plt.plot(dataframe.iloc[:,0], dataframe.iloc[:,2], color = "red")
    plt.title(f"Plot of Date vs. Returns for {returns_in_question}")
    plt.xlabel("Date")
    plt.ylabel("Returns")
    plt.show()