import numpy as np
import pandas as pd
from statsforecast.core import _StatsForecast
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA
from statsforecast.arima import arima_string
from matplotlib import pyplot
from arch import arch_model


def plot_acf_pacf(stocks, string_name):

    fig, ax = pyplot.subplots(1, 2, figsize=(10, 5))
    plot_acf(stocks[:,1], lags=20, ax=ax[0], use_vlines=True) 
    ax[0].set_xlabel("Lags")
    ax[0].set_ylabel("Autocorrelation")
    ax[0].set_title("ACF")
    ax[0].set_xticks(np.arange(1,21,1))

    plot_pacf(stocks[:,1], lags=20, ax=ax[1], use_vlines=True) 
    ax[1].set_xlabel("Lags")
    ax[1].set_ylabel("Partial Autocorrelation")
    ax[1].set_title("PACF")
    ax[1].set_xticks(np.arange(1,21,1))
    
    pyplot.subplots_adjust(wspace = 0.33)
    pyplot.suptitle(f"Plots of ACF (Autocorrelation Function) & PACF (Partial Autocorrelation Function) for {string_name}")
    pyplot.show()

    return

def arma_fit(returns_chosen, string_name):

    # we label this as 'df' for simplicity
    df = returns_chosen
    df = returns_chosen.to_pandas()

    # If statement, to ensure the columns are named correctly
    if (len(df.columns) > 2):
        df.columns = ['ds', 'prices', 'y'] # where y = returns
        df['unique_id'] = 'oil_stock' # will need to change this
        df = df.drop(columns='prices')
        df['ds'] = pd.to_datetime(df['ds'])
    else:
        df.columns = ['ds', 'y'] # where y = returns
        df['unique_id'] = 'oil_stock' # will need to change this
        df['ds'] = pd.to_datetime(df['ds'])


    # Printing out the ARIMA values selected with AutoArima
    print(f"Showing: {string_name}")
    sf = StatsForecast(
    models=[AutoARIMA(seasonal = False, max_p = 5, max_q = 5, stepwise = False, approximation=False)],
    freq='D',)
    sf.fit(df)
    print(" ")
    print("Auto ARIMA calculation: ")

    final_fit = sf.fitted_[0,0].model_
    print(arima_string(sf.fitted_[0,0].model_))

    # Return the end results - averaged stocks = ARMA(0,0), SP500 = ARMA(2,2), and oil = ARMA(2,3)
    return final_fit['arma']

def gjr_garch_test(stocks, oil, SP500, dummy_vars):

    
    
    return 
