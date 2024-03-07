#Beta Version

import numpy as np
import pandas as pd
from utils import time
from utils import utils
from utils.enumerations import Timeframe

d1_data = None
symbol_r = None
num_days = 0

#Function to calculate the Average Daily Rate
def get_values(daily_data, current_data, symbol, period):
    """
    Function to calculate the Average Daily Range of the given candles
    :param daily_data: dataframe object with daily candles
    :param current_data: dataframe with lower timeframe candles
    :param period: int, num of days to analyze
    :return: dataframe object with ADR values
    """

    global d1_data

    #Initialize global variable to daily data
    d1_data = daily_data

    global num_days
    #Initialize global variable to period
    num_days = period

    global count
    #Set count to -1
    count = -1

    global symbol_r
    #Initialize global variable to symbol
    symbol_r = symbol

    #Create a column called index with the same values as the dframe index
    daily_data["index"] = daily_data.apply(func_2345c, axis = 1)
    
    #Reset dframe index to time column
    daily_data.set_index("time", inplace = True)
    
    #Create a column called date to hold same values as time index
    daily_data["date"] = daily_data.index
    
    #Apply func_0728b to new column ADR to set Average Daily Range values
    current_data["ADR"] = current_data.apply(func_0728b, axis = 1)

    #Set dataframe variable to current data and return to caller
    dataframe = current_data

    return dataframe

#Function to set count values to each candle
def func_2345c(candle):
    global count
    count += 1
    return count

#Function to calculate ADR values for the given num days
def func_0728b(end_candle):

   
    #Get date value from the candles time
    current_date = time.get_date_string(end_candle.time)

    #Use date value to locate D1 candle of the same value and retrieve its index
    try:
        #Subtract the index by 1 to measure values from the previous date and back
        end = int(d1_data.loc[current_date, "index"]) - 1

    except KeyError as e:
        print("Symbol for Error:", symbol_r)
        print("Culprit:", end_candle)
        print(f"Error! {current_date} beyond the bounds of the Daily data set")
    
    adr = 0


    #Use the index to calculate the candle num days prior to current candle
    start = end - num_days

    #Initialize resultant to 0, to hold sum of ADR values
    result = 0
    
    #Grab the candles within the set period
    candles = d1_data.iloc[start:end]

    #Loop through each one of the candles and calculate the different between High and Low of the day
    for i in range(len(candles)):
        
        
        candle = candles.iloc[i]
        diff = round(((candle.high - candle.low) / utils.get_divider(symbol_r)), 1)
        result += diff
    
    #ADR is the average of the added differences
    adr = round((result / num_days))

    #Return adr value to caller
    return adr

    
    
    

def is_level_1(pips, adr_value, timeframe):

    if timeframe == Timeframe.H1:

        if (pips >= (1 * adr_value)) & (pips < (2 * adr_value)):
            return True
        else:
            return False
        
    elif timeframe == Timeframe.H4:

        if (pips >= (3 * adr_value)) & (pips < (6 * adr_value)):
                return True
        else:
            return False
        
def is_level_2(pips, adr_value, timeframe):

    if timeframe == Timeframe.H1:

        if (pips >= (2 * adr_value)) & (pips < (3 * adr_value)):
            return True
        else:
            return False
        
    elif timeframe == Timeframe.H4:

        if (pips >= (6 * adr_value)) & (pips < (9 * adr_value)):
            return True
        else:
            return False
        
    else:
        raise Exception("Incorrect Timeframe")
        
def is_level_3(pips, adr_value, timeframe):

    if timeframe == Timeframe.H1:

        if (pips >= (3 * adr_value)):
            return True
        else:
            return False
        
    elif timeframe == Timeframe.H4:

        if (pips >= (9 * adr_value)):
            return True
        else:
            return False
        
    else:
        raise Exception("Incorrect Timeframe") 

    



    


