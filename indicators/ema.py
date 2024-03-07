#Beta Version
import numpy as np
import pandas as pd
from utils import utils

#This function calculates an EMA of any period
def get_values(dataframe, period):
    ema_name = "EMA_" + str(period)
    multiplier = 2 / (period + 1)
    initial_mean = dataframe.close.head(period).mean()

    for i in range(len(dataframe)):
        if i == period:
            dataframe.loc[i, ema_name] = initial_mean

        elif i > period:
            ema_value = dataframe.loc[i, "close"] * multiplier + dataframe.loc[i - 1, ema_name] * (1 - multiplier)
            dataframe.loc[i, ema_name] = ema_value

        else:
            dataframe.loc[i, ema_name] = 0.00

    return dataframe

def calculate_cross(dataframe: pd.DataFrame, ema_one: int, ema_two: int) -> pd.DataFrame:
    """
    Function to calculate on an EMA cross event. EMA Column names must be in the formula EMA_<value>. I.e. values
    would be EMA_200 e.g.
    :param dataframe: dataframe object
    :param ema_one: Integer of EMA 1 period
    :param ema_two: Integer of EMA 2 period
    :return: dataframe with cross events
    """

    #Get the column names

    #EMA column 1
    column_one = "EMA_" + str(ema_one)
    #EMA column 2
    column_two = "EMA_" + str(ema_two)

    
    #Position column i.e differences between ema_one and ema_two
    try:
        dataframe["Pos"] = dataframe[column_one] - dataframe[column_two]

    except KeyError as e:
        print("KeyError: EMA columns undefined")

    
    #Pre-position column with the previous positions
    dataframe["Pre_Pos"] = dataframe["Pos"].shift(1)
    
    dataframe.dropna()

    column_name = str(ema_one) +"/"+ str(ema_two) +"-"+ "cross"
    
    #Define the crossover events
    dataframe[column_name] = dataframe.apply(is_cross, axis = 1)
 
    #Drop the position and pre-position columns
    dataframe.drop(columns = ["Pos", "Pre_Pos"], inplace = True)

    return dataframe

#Function to apply to series data for cross calculate
def is_cross(candle):
    """
    Function to apply to each candle of a dataframe to determine if a cross event has occurred
    :param candle: series object, candle from a dataframe
    """

    if candle.Pos >= 0 and candle.Pre_Pos < 0:
        return 1
    elif candle.Pos <= 0 and candle.Pre_Pos > 0:
        return -1
    else:
        return 0

#Function to calculate gradients of moving average
def calculate_gradient(dataframe: pd.DataFrame, symbol: str, ema: int, num_candles: int) -> pd.DataFrame:
    
    ma_column = "EMA_" +str(ema)
    column_name = "Delta-" + str(ema)
    dataframe[column_name] = 0

    for i in range(len(dataframe)):

        if i >= num_candles:

            start_index = i - num_candles
            ema_one = dataframe.loc[start_index, ma_column]
            ema_two = dataframe.loc[i, ma_column]

            #0.0012

            diff = ema_two - ema_one
            delta = round(diff * 1000000)
            dataframe.loc[i, column_name] = delta

    return dataframe



