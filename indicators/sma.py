#Beta Version
import numpy as np
import pandas as pd

#Function to calculate Simple Moving Average of any period
def get_values(dataframe, period):
    """
    Function to calculate a simple moving average based period passed as an argument.
    applied to the given dataframe
    :param dataframe: the dataframe object to be analyzed
    :param period: integer of the moving average periods
    :return: dataframe with the moving average
    """

    column_name = "SMA_" + str(period)

    for i in range(len(dataframe)):

        #If the index is less than the period init SMAs to 0.00
        if i < period:
            dataframe.loc[i, column_name] = 0.00
        #If the index is the same as the period calculate the mean from head()
        elif i == period:
            dataframe.loc[i , column_name] = dataframe["close"].head(period).mean()
        #Else grab the last {period} candles and calculate the mean
        else:
            start = i - period
            end = i
            dataframe.loc[i, column_name]  = dataframe.loc[start:end, "close"].mean()

    return dataframe

def get_rsi_values(dataframe, period):
    """
    Function to calculate a simple moving average based period passed as an argument.
    applied to the given dataframe
    :param dataframe: the dataframe object to be analyzed
    :param period: integer of the moving average periods
    :return: dataframe with the moving average
    """

    column_name = "sma_" + str(period) + "_tdi"

    for i in range(len(dataframe)):

        #If the index is less than the period init SMAs to 0.00
        if i < period:
            dataframe.loc[i, column_name] = 0.00
        #If the index is the same as the period calculate the mean from head()
        elif i == period:
            dataframe.loc[i , column_name] = dataframe["rsi"].head(period).mean()
        #Else grab the last {period} candles and calculate the mean
        else:
            start = i - period
            end = i
            dataframe.loc[i, column_name]  = dataframe.loc[start:end, "rsi"].mean()

    return dataframe

def get_cci_values(dataframe, period):
    """
    Function to calculate a simple moving average based period passed as an argument.
    applied to the given dataframe
    :param dataframe: the dataframe object to be analyzed
    :param period: integer of the moving average periods
    :return: dataframe with the moving average
    """

    column_name = "sma_" + str(period) + "_cci"

    for i in range(len(dataframe)):

        #If the index is less than the period init SMAs to 0.00
        if i < period:
            dataframe.loc[i, column_name] = 0.00
        #If the index is the same as the period calculate the mean from head()
        elif i == period:
            dataframe.loc[i , column_name] = dataframe["cci"].head(period).mean()
        #Else grab the last {period} candles and calculate the mean
        else:
            start = i - period
            end = i
            dataframe.loc[i, column_name]  = dataframe.loc[start:end, "cci"].mean()

    return dataframe


def calculate_cross(dataframe, sma_one, sma_two):
    """
    Function to calculate on an SMA cross event. SMA Column names must be in the formula SMA_<value>. I.e. values
    would be SMA_200 e.g.
    :param dataframe: dataframe object
    :param sma_one: Integer of SMA 1 period
    :param sma_two: Integer of SMA 2 period
    :return: dataframe with cross events
    """

    #Get the column names

    #SMA column 1
    column_one = "SMA_" + str(sma_one)
    #SMA column 2
    column_two = "SMA_" + str(sma_two)

    
    #Position column i.e differences between sma_one and sma_two
    try:
        dataframe["Pos"] = dataframe[column_one] - dataframe[column_two]

    except KeyError as e:
        print("KeyError: SMA columns undefined")

    
    #Pre-position column with the previous positions
    dataframe["Pre_Pos"] = dataframe["Pos"].shift(1)
    
    dataframe.dropna()
    
    #Define the crossover events
    dataframe["Cross"] = dataframe.apply(is_cross, axis = 1)
 
    #Drop the position and pre-position columns
    dataframe.drop(columns = ["Pos", "Pre_Pos"])

    return dataframe

#Function to apply to series data for cross calculate
def is_cross(row):
    """
    Function to apply to each row of a dataframe to determine if a cross event has occurred
    :param row: series object, row from a dataframe
    """

    if row.Pos >= 0 and row.Pre_Pos < 0:
        return 1
    elif row.Pos <= 0 and row.Pre_Pos > 0:
        return -1
    else:
        return 0