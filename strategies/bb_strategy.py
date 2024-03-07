import numpy as np
import pandas as pd
from utils import utils
from strategies.strategy import Strategy
from indicators import rsi, cci, sma, bollinger

class BB_Strategy(Strategy):

    @property
    def symbol(self) -> str:
        return self.__symbol
    
    @symbol.setter
    def symbol(self, symbol: str):
        self.__symbol = symbol

    #Constructor
    def __init__(self, symbol = "Volatility 100 Index"):
        self.symbol = symbol
        self.count = 0

    #Function to test Bounce Strategy
    def test(self, candles = None, timeframe = "M1"):

        if candles is None:
            candles = self.retrieve_candle_data(
                symbol = self.symbol,
                timeframe = timeframe,
                limit = 100
            )

        data = self.calculate_indicators(data = candles)

        signals = self.determine_trade(data = data)

        return signals
    
    #Function to run Market Maker Strategy
    def run(self, timeframe = "M1"):
        

        #Step 3: Retrieve M15 candle data
        candles = self.retrieve_candle_data(
            symbol = self.symbol,
            timeframe = timeframe,
            limit = 200
        )

        data = self.calculate_indicators(data = candles)

        #Step 8: Determine trade on M15 timeframe
        signals = self.determine_trade(data = data)

        signal_candle = signals.tail(1)

        if self.count == 1:
            signal_candle["dtrade"] = "Fall"

        self.count += 1

        return signal_candle

    #Function to calculate indicators
    def calculate_indicators(self, data):

        #Calculate RSI
        data = rsi.get_values(dataframe = data, period = 21)

        #Calculate Signal line SMA-7
        data = sma.get_rsi_values(dataframe = data, period = 7)
        data.rename(columns = {"sma_7_tdi": "signal_line"}, inplace = True)

        #Calculate Base line SMA-34
        data = sma.get_rsi_values(dataframe = data, period = 34)
        data.rename(columns = {"sma_34_tdi":"base_line"}, inplace = True)
        
        #Calculate Bollinger Upper Band
        data = bollinger.get_rsi_upper(dataframe = data, period = 34, deviation = 1.619)

        #Calucate Bollinger Lower Band
        data = bollinger.get_rsi_lower(dataframe = data, period = 34, deviation = 1.619)

        #Calculate CCI Price line
        data = cci.get_values(dataframe = data, period = 100)

        #Calcuate CCI Base line
        data = sma.get_cci_values(dataframe = data, period = 20)
        data.rename(columns = {"sma_20_cci":"MBL"}, inplace = True)

        data.round()

        return data
    
    #Function to calculate trade signals
    def determine_trade(self, data):

        data["dtrade"] = "-"
        bear_points = 0
        bull_points = 0
        height = 20
        leg = 0
        apex = 0

        for i in range(len(data)):

            """Retrieve Values"""

            mbl_line = round(data.loc[i, "MBL"])
            rsi_line = round(data.loc[i, "rsi"])
            price_line = round(data.loc[i, "cci"])
            signal_line = round(data.loc[i, "signal_line"])
            base_line = round(data.loc[i, "base_line"])
            upper_value = round(data.loc[i, "upper_tdi"])
            lower_value = round(data.loc[i, "lower_tdi"])

            """"""""""""""""""""""""

            #FOR BUY SIGNALS

            """
            For a BUY Signal, all three points need to be marked and the CCI price line
            has crossed at or above the Market Base line. 
            Height between the potential M Leg and apex has to be greater than 10 pips.
            Reset all variables, inspite of signal."""

            if (price_line >= mbl_line) & (bear_points == 3):


                if isinstance(leg, pd.Series) & isinstance(apex, pd.Series):
                    pip_value = leg.high - apex.close
                    height = round(pip_value / utils.get_divider(self.symbol))

                if(price_line < 0):
                    data.loc[i, "dtrade"] = "Rise"

                elif(price_line > 0) & (height > 10):
                    data.loc[i, "dtrade"] = "Rise"
                    
                
                bear_points = 0
                height = 20 
                leg = 0
                apex = 0

            """Create the variables to determine points in contact on the TDI"""

            #The point in which the SMA 34 touhes the RSI
            contact = base_line - rsi_line

            #The point at which the CCI touches the Base line
            bounce = mbl_line - price_line

            #The drop in CCI when it goes below the Base line
            distance = mbl_line - price_line

            #The point on which the RSI touches the Upper Bollinger
            touch = upper_value - rsi_line

            """///////////////////////////////////////////////////////////////"""

            if (touch <= 2) & (bear_points > 0):

                if isinstance(leg, int):
                    leg = data.loc[i]
                else:
                    if data.loc[i, "high"] > leg.high:
                        leg = data.loc[i]


            """
            When the RSI line goes below the Lower Bollinger Band and the CCI is also below the Market 
            base line, mark the first point and reset the variables."""
            
            if (rsi_line <= lower_value) & (price_line < mbl_line):

                bear_points = 1
                height = 20
                leg = 0
                apex = 0


            """
            When the RSI line comes close to, or crosses above the SMA 34 base line, and 
            the CCI price line comes close to, or cross above the Market base line, mark
            the second point."""
            
            if (contact <= 1) & (bounce <= 5) & (bear_points == 1):
                
                bear_points = 2

            if (price_line < mbl_line) & (rsi_line < signal_line) & (bear_points == 2):
                if distance >= 15:
                    bear_points = 3

            if (price_line < mbl_line) & (bear_points == 3):

                if isinstance(apex, int):
                    apex = data.loc[i]

                else:
                    if data.loc[i, "low"] < apex.low:
                        apex = data.loc[i]


            

        return data





            



