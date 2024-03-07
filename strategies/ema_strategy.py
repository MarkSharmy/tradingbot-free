
#Beta Version
import numpy as np
import pandas as pd
import indicators
import tradebot
from strategies.strategy import Strategy

class EMA_Strategy(Strategy):

    #Constructor
    def __init__(self, ema_one = 16, ema_two = 64):
        self.ema_one = ema_one
        self.ema_two = ema_two



    #Function to test the EMA cross Strategy
    def test(self, data = None, symbol = "EURUSD"):
        """
        Function which tests the EMA Cross Strategy
        :param data: dataframe object to be analyzed
        :param timeframe: string of the timeframe to be queried
        :param ema_one: Integer of the lowest timeframe length for EMA
        :param ema_two: Integer of the highest timeframe length for the EMA
        :return: trade event dataframe
        """

        #Step 1: Retrive the candlesticks data
        if data is None:
            data = self.retrieve_candle_data(
            symbol = symbol,
            timeframe = "H1"
        )

        #Step 2: Calculate indicators
        data = self.calculate_indicators(
            data = data, 
            ema_one = self.ema_one,
            ema_two = self.ema_two
        )

        #Step 3: Determine if a trade event has occurred
        data = self.determine_trade(
            dataframe = data,
        )

        return data

    def calculate_indicators(self, data, ema_one, ema_two):
        """
        Function to calculate the indicators for the EMA Cross Strategy
        :param data: dataframe of the raw data
        :param ema_one: integer for the first ema
        :param ema_two: integer for the second ema
        :return: dataframe with updated columns
        """

        #Calculate the first ema
        data = indicators.calculate_ema(dataframe = data, period = ema_one)
        #Calculate the second ema 
        data = indicators.calculate_ema(dataframe = data, period = ema_two)
        #Calculate the EMA Cross
        data = indicators.calculate_cross(dataframe = data, ema_one = ema_one, ema_two = ema_two)

        return data

    #Function to determine if a trade event has occurred, and if so, calculate trade signal
    def determine_trade(self, dataframe):
        """
        Function to calculate a trade signal for the strategy. For the EMA cross, we apply the following rules:
        1. For each trade, stop_loss is the corresponding hightest EMA (i.e. is ema_one is 50 and
        ema_two is 200)
        2. For a BUY signal, the entry_price (stop_price) is the high of the previous candle
        3. For a SELL signal, the entry_price (stop_price) is the low of the previous candle
        4. The take_profit is the absolute distance between the stop_price and stop_loss,
        added 

        :param dataframe: dataframe of data with indicators
        :param ema_one: integer of the smaller EMA
        :param ema_two: integer of the larger EMA
        :return: dataframe object with trade values added
        """

        dataframe["SIGNALS"] = "-"

        for i in range(len(dataframe)):
            if dataframe.loc[i, "Cross"] == 1:
                dataframe.loc[i, "SIGNALS"] = "BUY"

            elif dataframe.loc[i, "Cross"] == -1:
                dataframe.loc[i, "SIGNALS"] = "SELL"

            else:
                #No signal
                continue


        return dataframe


