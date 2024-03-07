#Beta Version 
import numpy as np
import pandas as pd
from typing import Callable

def get_values(dataframe: pd.DataFrame, period: int):

    rsi_values = calculate_rsi(dataframe, period)
    dataframe["rsi"] = rsi_values

    return dataframe

#Function to calculate Relative Strength Index
def calculate_rsi(dataframe: pd.DataFrame, period: int):

    # Extract close prices from the historical data
    close_prices = dataframe["close"]
    
    delta = close_prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    rsi = rsi.fillna(0)

    return rsi
