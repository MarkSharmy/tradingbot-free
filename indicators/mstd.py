#Beta Version

import math
import numpy as np
import pandas as pd
from indicators import sma
from indicators import ema
from utils.enumerations import MA

candle_data = None
num_candles = 0
ma_column = None

#Function to calculate Moving Standard Deviation
def get_values(dataframe, period, MA_Type):
    
    global candle_data
    global num_candles
    global ma_column

    dataframe["index"] = dataframe.index

    if MA_Type == MA.SMA:
        dataframe = sma.get_values(dataframe, period)
        column_name = "SMA_" + str(period)

    elif MA_Type == MA.EMA:
        dataframe = ema.get_values(dataframe, period)
        column_name = "EMA_" + str(period)

    else:
        raise Exception("Error, incorrect Moving Average Type")

    candle_data = dataframe
    num_candles = period
    ma_column = column_name

    dataframe["MSD"] = dataframe.apply(func_0245e, axis = 1)
    dataframe.drop(columns = [ma_column])

    return dataframe

#Function to calculate the Moving Standard Deviation
def func_0245e(series):

    index = series["index"]

    if index < num_candles:
        return 0.0
    
    else:

        total = 0.0
        average = 0.0
        start = index - num_candles
        end = index

        data = candle_data.loc[start:end]

        for i in range(len(data)):
            candle = data.iloc[i]
            price = candle["close"]
            ma = candle[ma_column]
            total += math.pow((price - ma), 2)

        average = total / num_candles
        resultant =math.sqrt(average)

        return resultant