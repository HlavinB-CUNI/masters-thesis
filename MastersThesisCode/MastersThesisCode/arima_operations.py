import csv
import os
import polars as pl
import yfinance as yahoo
from statsmodels.tsa.stattools import adfuller
from file_operations import file_existence_check, export_values_to_csv