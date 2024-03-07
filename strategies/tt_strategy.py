#Beta Version

import numpy as np
import pandas as pd
from tdi import TDI
from utils import time
from utils import utils
from tdi import Bollinger
from utils.objects import Point, Setup, MiniSetup
from strategies.strategy import Strategy
from indicators import sma, ema, rsi, adr, bollinger
from utils.enumerations import Trend, Levels, Timeframe

class TT_Strategy(Strategy):


    @property
    def symbol(self):
        return self.__symbol
    
    @symbol.setter
    def symbol(self, symbol: str):
        self.__symbol = symbol

    #Constructor 
    def __init__(self, symbol = "EURUSD"):
        self.symbol = symbol
        self.count = 0



    #Function to test Market Maker Strategy
    def test(self, candles = None, timeframe = "M1"):
        
        if candles is None:
            #Step 3: Retrieve M15 candle data
            candles = self.retrieve_candle_data(
                symbol = self.symbol,
                timeframe = timeframe,
                limit = 100
            )

        #Step 6: Calculate indicators for M15
        data = self.calculate_indicators(data = candles)

        #Step 7: Determine trade on M15 timeframe
        signals = self.determine_trade(data = data)

        return signals

        
    #Function to run Market Maker Strategy
    def run(self, timeframe = "M1"):
        

        #Step 3: Retrieve M15 candle data
        candles = self.retrieve_candle_data(
            symbol = self.symbol,
            timeframe = timeframe,
            limit = 100
        )

        data = self.calculate_indicators(data = candles)

        #Step 8: Determine trade on M15 timeframe
        signals = self.determine_trade(data = data)

        signal_candle = signals.tail(1)

        if self.count == 1:
            signal_candle["dtrade"] = "Fall"

        self.count += 1

        return signal_candle

    
    #Function to calculate indicators for M15
    def calculate_indicators(self, data):

        #Calculate 5 Exponetial Moving Average
        data = ema.get_values(dataframe = data, period = 5)
        #Calculate gradients of EMA 5
        data = ema.calculate_gradient(dataframe = data, symbol = self.symbol, ema = 5, num_candles = 1)
        #Calculate 13 Exponential Moving Average
        data = ema.get_values(dataframe = data, period = 13)
        #Calculate 50 Exponential Moving Average
        data = ema.get_values(dataframe = data, period = 50)
        #Calculate 200 Exponential Moving Average
        data = ema.get_values(dataframe = data, period = 200)
        #Calculate 800 Exponetial Moving Average
        data = ema.get_values(dataframe = data, period = 800)
        #Calculate 13/50 EMA Cross
        data = ema.calculate_cross(dataframe = data, ema_one = 13, ema_two = 50)
        #Calculate 5/13 EMA Cross
        data = ema.calculate_cross(dataframe = data, ema_one = 5, ema_two = 13)
        #Calculate RSI Line SMA-2
        data = rsi.get_values(dataframe = data, period = 21)
        #Calculate Signal Line SMA-7
        data = sma.get_rsi_values(dataframe = data, period = 7)
        data.rename(columns = {"sma_7_tdi":"signal_line"}, inplace = True)
        data = utils.calculate_cross(dataframe = data, indicator_1 = "rsi", indicator_2 = "signal_line")
        data.rename(columns = {"tdi_cross":"signal_cross"}, inplace = True)
        #Calculate Market Base Line SMA-34
        data = sma.get_rsi_values(dataframe = data, period = 34)
        data.rename(columns = {"sma_34_tdi":"base_line"}, inplace = True)
        #Calculate Bollinger Upper-Band
        data = bollinger.get_rsi_upper(dataframe = data, period = 34, deviation = 1.619)
        #Calculate Bollinger Lower-Band
        data = bollinger.get_rsi_lower(dataframe = data, period = 34, deviation = 1.619)
        #Add levels and trends to M15 data

        return data

    def determine_trade(self, data):

        data["SIGNALS"] = "-"
        data["dtrade"] = "-"
        setups = []
        first_leg = 0  


        for i in range(len(data)):

            trend = Trend.BULL
   

            """ RSI LINE """

            rsi_line = int(data.loc[i, "rsi"])

            """"""""""""""""""
            
            """ SIGNAL LINE"""

            signal_line = int(data.loc[i, "signal_line"])


            """"""""""""""""""""

            """ BOLLINGER LOWER BAND """

            upper_value = int(data.loc[i, "upper_tdi"])
            lower_value = int(data.loc[i, "lower_tdi"])

            """"""""""""""""""
            
            if trend == Trend.BULL:

                for setup in setups:
                    setup.update(
                        dataframe = data,
                        candle = data.loc[i],
                        start_index = (i - 15),
                        trend = trend
                    )

                if (rsi_line <= lower_value) & (rsi_line < signal_line):

                    if isinstance(first_leg, int):
                        first_leg = data.loc[i]

                    elif (data.loc[i, "low"] < first_leg.low):
                        first_leg = data.loc[i]


                if (rsi_line > signal_line):

                    if isinstance(first_leg, pd.Series):
                        setups.append(MiniSetup(self.symbol, first_leg))
                        first_leg = 0

                    for setup in setups:
                        if setup.is_complete:
                            if setup.has_signal:
                                if (data.loc[i, "time"] == setup.signal_candle.time):
                                    data.loc[i, "dtrade"] = "Rise"

            if trend == Trend.BEAR:
                for setup in setups:
                    setup.update(
                        dataframe = data,
                        candle = data.loc[i],
                        start_index = (i - 15),
                        trend = trend
                    )

                if (rsi_line >= upper_value) & (rsi_line > signal_line):

                    if isinstance(first_leg, int):
                        first_leg = data.loc[i]

                    elif (data.loc[i, "high"] > first_leg.high):
                        first_leg = data.loc[i]


                if (rsi_line < signal_line):

                    if isinstance(first_leg, pd.Series):
                        setups.append(MiniSetup(self.symbol, first_leg))
                        first_leg = 0

                    for setup in setups:
                        if setup.is_complete:
                            if setup.has_signal:
                                if (data.loc[i, "time"] == setup.signal_candle.time):
                                    data.loc[i, "dtrade"] = "Fall"

        print("Setups:", len(setups))
        setups.clear()
                
 
        """\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ END OF LOOP \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"""

        #Return Dataframe with trade signals
        return data



            