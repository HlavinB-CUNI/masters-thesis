from math import sqrt
import numpy as np
import pandas as pd
import polars as pl
import scipy.stats
from statsforecast.core import _StatsForecast
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA
import statsmodels.api as sm_api
from matplotlib import pyplot
from arch import arch_model
from file_operations import file_existence_check, export_values_to_csv
import os
import scipy


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

    # White Noise ARMA(0,0) test and Ljung-Box test just to confirm autocorrelation exists
    arma_white_noise = sm_api.tsa.arima.ARIMA(df["y"], order = (0,0,0)).fit()

    ljung_box_initial5 = sm_api.stats.acorr_ljungbox(arma_white_noise.resid, lags=[5], return_df=True)
    ljung_box_initial10 = sm_api.stats.acorr_ljungbox(arma_white_noise.resid, lags=[10], return_df=True)
    ljung_box_initial15 = sm_api.stats.acorr_ljungbox(arma_white_noise.resid, lags=[15], return_df=True)
    ljung_box_initial20 = sm_api.stats.acorr_ljungbox(arma_white_noise.resid, lags=[20], return_df=True)
    print(ljung_box_initial5)
    print(ljung_box_initial10)
    print(ljung_box_initial15)
    print(ljung_box_initial20)

    ljung_box_initial5_sq = sm_api.stats.acorr_ljungbox(arma_white_noise.resid**2, lags=[5], return_df=True)
    ljung_box_initial10_sq = sm_api.stats.acorr_ljungbox(arma_white_noise.resid**2, lags=[10], return_df=True)
    ljung_box_initial15_sq = sm_api.stats.acorr_ljungbox(arma_white_noise.resid**2, lags=[15], return_df=True)
    ljung_box_initial20_sq = sm_api.stats.acorr_ljungbox(arma_white_noise.resid**2, lags=[20], return_df=True)
    print(ljung_box_initial5_sq)
    print(ljung_box_initial10_sq)
    print(ljung_box_initial15_sq)
    print(ljung_box_initial20_sq)

    # Printing out the ARIMA values selected with AutoArima
    print(f"Showing: {string_name}")
    sf = StatsForecast(
    models=[AutoARIMA(seasonal = False, max_p = 6, max_q = 6, stepwise = False, approximation=False)],freq='D')
    sf.fit(df)
    print(" ")
    print("Auto ARIMA calculation: ")

    # Getting and printing the AR, I, and MA terms to be used
    final_fit = sf.fitted_[0,0].model_
    print(sf.fitted_[0][0].model_['arma'])

    arma_23 = sm_api.tsa.arima.ARIMA(df["y"], order = (2,0,3)).fit()

    ljung_box_try5 = sm_api.stats.acorr_ljungbox(arma_23.resid, lags=[5], return_df=True)
    ljung_box_try10 = sm_api.stats.acorr_ljungbox(arma_23.resid, lags=[10], return_df=True)
    ljung_box_try15 = sm_api.stats.acorr_ljungbox(arma_23.resid, lags=[15], return_df=True)
    ljung_box_try20 = sm_api.stats.acorr_ljungbox(arma_23.resid, lags=[20], return_df=True)
    print(ljung_box_try5)
    print(ljung_box_try10)
    print(ljung_box_try15)
    print(ljung_box_try20)

    # Return the end results - averaged stocks = ARMA(0,0), SP500 = ARMA(2,2), and oil = ARMA(2,3)
    return final_fit['arma']


def garch_test(combined_df, ar_value, ma_value):

    # NOTE - RESCALING WAS NEEDED FOR THE DEPENDENT VARIABLE SO THE NEW COLUMN IS "return*100", done for other returns as well!
    # Re-scaling with new columns
    combined_df = combined_df.with_columns(pl.col('_Mean-Oil-Stocks').mul(100).alias('_Mean-Oil-Stocks*100'))
    combined_df = combined_df.with_columns(pl.col('Diff_^SPX').mul(100).alias('Diff_^SPX*100'))
    combined_df = combined_df.with_columns(pl.col('Diff_CL=F').mul(100).alias('Diff_CL=F*100'))

    only_dummies_df = combined_df.drop(['_Mean-Oil-Stocks', '_Mean-Oil-Stocks*100', 'Diff_^SPX', 'Diff_^SPX*100', 'Diff_CL=F','Diff_CL=F*100'])
    print(only_dummies_df)

    model = arch_model(
        combined_df['_Mean-Oil-Stocks*100'], # select the oil stock averaged returns
        vol='GARCH',    
        x=combined_df[['Russia', 'DOE', 'OPEC', 'CoVID', 'Oil_Crash', 'Diff_^SPX*100', 'Diff_CL=F*100']],
        lags = ar_value, # Lags obtained from auto arima fitting
        p=1,             
        o=1,             # GJR-GARCH specification
        q=1,           
        dist='t',        # Student's t for fat tails
        mean='ARX')      # Autoregressive model
    
    # Fitting the model
    results = model.fit(update_freq=1, disp='off')
    print(results.summary())

    df_dates = pd.DataFrame(data = combined_df['Date'].to_pandas()).reset_index(drop = True)
    df_vol = pd.DataFrame(data = results.conditional_volatility).reset_index(drop = True)
    
    std_resid = results.resid / results.conditional_volatility
    std_resid = pd.Series(std_resid).replace([np.inf, -np.inf], np.nan).dropna()

    # Post-test diagnostics
    print("POST TEST DIAGNOSTICS:")

    ljung_box_garch_5 = sm_api.stats.acorr_ljungbox(std_resid, lags=[5], return_df=True)
    ljung_box_garch_10 = sm_api.stats.acorr_ljungbox(std_resid, lags=[10], return_df=True)
    ljung_box_garch_15 = sm_api.stats.acorr_ljungbox(std_resid, lags=[15], return_df=True)
    ljung_box_garch_20 = sm_api.stats.acorr_ljungbox(std_resid, lags=[20], return_df=True)

    ljung_box_garchsq_5 = sm_api.stats.acorr_ljungbox(std_resid**2, lags=[5], return_df=True)
    ljung_box_garchsq_10 = sm_api.stats.acorr_ljungbox(std_resid**2, lags=[10], return_df=True)
    ljung_box_garchsq_15 = sm_api.stats.acorr_ljungbox(std_resid**2, lags=[15], return_df=True)
    ljung_box_garchsq_20 = sm_api.stats.acorr_ljungbox(std_resid**2, lags=[20], return_df=True)
    
    print('Ljung-Box Results, Post GJR-GARCH')
    print(ljung_box_garch_5)
    print(ljung_box_garch_10)
    print(ljung_box_garch_15)
    print(ljung_box_garch_20)

    print(ljung_box_garchsq_5)
    print(ljung_box_garchsq_10)
    print(ljung_box_garchsq_15)
    print(ljung_box_garchsq_20)

    # Assembling dataframe for the volatility values generated
    df_vol = pd.concat([df_dates, df_vol], axis = 1)
    df_vol.rename(columns = {0:'Volatility'}, inplace = True)
    df_vol['True_Volatility'] = df_vol['Volatility'] / 100 # Need to move scale back to default by dividing by 100

    df_annualized_vol = df_vol
    df_annualized_vol['Ann_Vol'] = df_vol['True_Volatility']*sqrt(252)

    print("Summary Statistic for Returns")
    print("Oil & Gas Stocks")
    print(combined_df['_Mean-Oil-Stocks'].describe())
    print(scipy.stats.skew(combined_df['_Mean-Oil-Stocks']))
    print(scipy.stats.kurtosis(combined_df['_Mean-Oil-Stocks']))

    print("S&P500")
    print(combined_df['Diff_^SPX'].describe())
    print(scipy.stats.skew(combined_df['Diff_^SPX']))
    print(scipy.stats.kurtosis(combined_df['Diff_^SPX']))

    print("Crude Oil")
    print(combined_df['Diff_CL=F'].describe())
    print(scipy.stats.skew(combined_df['Diff_CL=F']))
    print(scipy.stats.kurtosis(combined_df['Diff_CL=F']))

    print("Volatility Summary")
    print(df_vol['True_Volatility'].describe())

    print("Annualized Volatility Summary")
    print(df_annualized_vol['Ann_Vol'].describe())

    # Establishing the directory path for all files for this project
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Exporting volatility values to .csv
    file_existence_check(f"{script_dir}\Data\volatility_garch_results.csv")
    export_values_to_csv('volatility_garch_results.csv', pl.from_pandas(df_vol))

    # Exporting the new scaled data to .csv 
    file_existence_check(f"{script_dir}\Data\rescaled_dataframe_all_vars.csv")
    export_values_to_csv('rescaled_dataframe_all_vars.csv', combined_df)
    
    return results, combined_df, pl.from_pandas(df_vol)
