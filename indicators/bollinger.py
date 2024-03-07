#Beta Version

import numpy as np
import pandas as pd
from indicators import sma
from indicators import rsi

#Function to calculate Bollinger Upper Band
def get_upper(dataframe, period, deviation):

    df = sma.get_values(dataframe = dataframe, period = period)
    ma_column = "SMA_" + str(period)
    df["std"] = df["close"].rolling(window = period).std()
    df["Upper"] = df[ma_column] + (deviation * df["std"])
    df["Upper"] = df["Upper"].fillna(0)
    df.drop(columns = [ma_column, "std"], inplace = True)

    return df


def get_rsi_upper(dataframe, period, deviation) -> pd.Series:
    
    data = dataframe["rsi"]
    rolling_mean = data.rolling(window = period).mean()
    rolling_std = data.rolling(window = period).std()
    dataframe["upper_tdi"] = rolling_mean + (rolling_std *  deviation)
    dataframe["upper_tdi"] = dataframe["upper_tdi"].fillna(0)
    
    return dataframe

#Function to calculate Bollinger Mid Band
def get_middle(dataframe, period, deviation):
    
    df = sma.get_values(dataframe = dataframe, period = period)
    ma_column = "SMA_" + str(period)
    df.rename(columns = {ma_column:"Middle"}, inplace = True)
    return df

#Function to calculate Bollinger Upper Band
def get_lower(dataframe, period, deviation):

    df = sma.get_values(dataframe = dataframe, period = period)
    ma_column = "SMA_" + str(period)
    df["std"] = df["close"].rolling(window = period).std()
    df["Lower"] = df[ma_column] - (deviation * df["std"])
    df["Lower"] = df["Lower"].fillna(0)
    df.drop(columns = [ma_column, "std"], inplace = True)

    return df

def get_rsi_lower(dataframe, period, deviation) -> pd.Series:
    
    data = dataframe["rsi"]
    rolling_mean = data.rolling(window = period).mean()
    rolling_std = data.rolling(window = period).std()
    dataframe["lower_tdi"] = rolling_mean - (rolling_std *  deviation)
    dataframe["lower_tdi"] = dataframe["lower_tdi"].fillna(0)
    
    return dataframe

