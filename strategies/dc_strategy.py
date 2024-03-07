import numpy as np
import pandas as pd
from strategies.strategy import Strategy
from indicators import rsi, sma, bollinger

class DC_Strategy(Strategy):

    @property
    def symbol(self) -> str:
        return self.__symbol

    @symbol.setter
    def symbol(self, symbol: str):
        self.__symbol = symbol


    def __init__(self, symbol = "Volatility 100 Index"):
        self.symbol = symbol

    #Function to test the Deep Cycle Strategy
    def test(self, candles = None, timeframe = "M1") -> pd.DataFrame:

        if candles is None:
            candles = self.retrieve_candle_data(
                symbol = self.symbol,
                timeframe = timeframe
            )

        data = self.calculate_indicators(data = candles)

        signals = self.determine_trades(data = data)

        return signals
    
    #Function to run the Deep Cycle Strategy
    def run(self, timeframe = "M1") -> pd.Series:

        candles = self.retrieve_candle_data(
                symbol = self.symbol,
                timeframe = timeframe
            )
            
        data = self.calculate_indicators(data = candles)

        signals = self.determine_trades(data = data)

        signal = signals.tail(1)

        return signal
    
    #Function to calculate indicators
    def calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:

        #Calculate RSI values
        data = rsi.get_values(dataframe = data, period = 21)

        #Calculate signal line values
        data = sma.get_rsi_values(dataframe = data, period = 7)

        #Calculate Bollinger Upper-Band
        data = bollinger.get_rsi_upper(dataframe = data, period = 34, deviation = 1.619)

        #Calculate Bollinger Lower-Band
        data = bollinger.get_rsi_lower(dataframe = data, period = 34, deviation = 1.619)

        return data
    
    #Function to calcuate trade signals
    def determine_trades(self, data: pd.DataFrame) -> pd.DataFrame:

        data["dtrade"] = "-"
        point = 0

        for i in range(len(data)):

            #Get RSI value as an integer
            rsi = int(data.loc[i, "rsi"])

            #Get SMA 7 values 
            signal_line = int(data.loc[i, "sma_7_tdi"])

            #Get Upper Bollinger as an integer
            upper_value = int(data.loc[i, "upper_tdi"])

            if rsi > upper_value:

                point = 1


            if ((rsi <= signal_line) & (point == 1)):
                data.loc[i, "dtrade"] = "Fall"
                point = 0

        return data

    
