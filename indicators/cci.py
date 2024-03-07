#Beta Version
import numpy as np
import pandas as pd

#Function to calculate Commodity Channel Index
def get_values(dataframe, period):
    
    dataframe = calculate_cci(dataframe, period)

    return dataframe


def calculate_cci(df, period):
    typical_price = (df['high'] + df['low'] + df['close']) / 3

    # Calculate the mean deviation
    mean_deviation = typical_price.rolling(window=period).apply(lambda x: np.mean(np.abs(x - np.mean(x))))

    # Calculate the CCI
    cci = (typical_price - typical_price.rolling(window=period).mean()) / (0.015 * mean_deviation)

    df['cci'] = cci.fillna(0)
    
    return df