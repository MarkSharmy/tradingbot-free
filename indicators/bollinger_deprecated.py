#Beta Version

import numpy as np
import pandas as pd
from indicators import sma
from indicators import mstd
from utils.enumerations import MA

ma_column = None

#Function to calculate Bollinger Band Upper Band
def get_upper(dataframe, period):
    global ma_column
    ma_column = "SMA_" + str(period)

    dataframe = sma.get_values(dataframe, period)
    dataframe = mstd.get_values(dataframe, period, MA.SMA)
    dataframe["BB_Upper"] = dataframe.apply(func_0821a, axis = 1)
    dataframe.drop(columns = [ma_column, "MSD"], inplace = True)
    return dataframe

def func_0821a(candle):
    
    ma = candle[ma_column]
    sd = candle["MSD"]
    result = (ma + (sd * 2))
    return result


    

#Function to calculate Bollinder Band Middle Band
def get_middle(dataframe, period):
    global ma_column
    ma_column = "SMA_" + str(period)

    dataframe = sma.get_values(dataframe, period)
    dataframe = mstd.get_values(dataframe, period, MA.SMA)
    dataframe["BB_Mid"] = dataframe.apply(func_0821b, axis = 1)
    dataframe.drop(columns = [ma_column, "MSD"], inplace = True)
    return dataframe

def func_0821b(candle):
    
    ma = candle[ma_column]
    result = ma
    return result

#Function to calculate Bollinger Band Lower Band
def get_lower(dataframe, period):
    global ma_column
    ma_column = "SMA_" + str(period)

    dataframe = sma.get_values(dataframe, period)
    dataframe = mstd.get_values(dataframe, period, MA.SMA)
    dataframe["BB_Lower"] = dataframe.apply(func_0821c, axis = 1)
    dataframe.drop(columns = [ma_column, "MSD"], inplace = True)
    return dataframe

def func_0821c(candle):
    
    ma = candle[ma_column]
    sd = candle["MSD"]
    result = (ma - (sd * 2))
    return result