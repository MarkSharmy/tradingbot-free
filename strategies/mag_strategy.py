#Beta Version
import numpy as py
import pandas as pd
import indicators
import tradebot
from strategies.strategy import Strategy

class Mag_Strategy(Strategy):

    #Function to test the MAG strategy
    def test(self, data = None, symbol = "EURUSD"):
        """
        Function which tests the Moving Average Gradient Strategy
        :param data: dataframe object to be analyzed
        :param timeframe: string og the timeframe to be queried
        :param sma_one: Integer of the lowest timeframe length for SMA
        :param sma_two: Integer of the highest timeframe length for SMA
        :param ema_one: Integer of the lowest timeframe length for EMA
        :param ema_two: Integer of the highest timeframe length for EMA
        :return: trade event dataframe
        """
        #Step 1: Retrieve the candlesticks data
        if data is None:
            data = self.retrieve_candle_data(
                symbol = symbol,
                timeframe = "M15"
            )

        #Step 2: Calculate indicators
        data = self.calculate_indicators(
            data = data,
            sma_one = 5,
            sma_two = 13,
            ema_one = 16,
            ema_two = 64
        )

        #Step 3: Determine if a trade event has occured
        data = self.determine_trade(data)

        data.set_index("time", inplace = True)
        return data


    def retrieve_candle_data(symbol, timeframe):
        """
        Function to retrieve data from MT5. Data is in the form of candlesticks and is retrieved as a dataframe
        :param symbol: string of the symbol to be retrieved
        :param timeframe: string of the timeframe to retrieved
        :return: dataframe of data
        """

        candles = tradebot.get_cadlesticks(symbol = symbol, timeframe = timeframe, limit = 5000)

        return candles

    def calculate_indicators(self, data, sma_one, sma_two, ema_one, ema_two):
        """
        Function to calculate the indicators for the MAG Strategy
        :param data: dataframe of the raw data
        :param sma_one: Integer of the lowest timeframe length for SMA
        :param sma_two: Integer of the highest timeframe length for SMA
        :param ema_one: Integer of the lowest timeframe length for EMA
        :param ema_two: Integer of the highest timeframe length for EMA
        :return: dataframe with updated columns
        """

        #Calculate the first sma
        df = indicators.calculate_sma(dataframe = data, size = sma_one)

        #Calculate the second sma
        df = indicators.calculate_sma(dataframe = df, size = sma_two)

        #Calculate the first ema
        df = indicators.calculate_ema(dataframe = df, size = ema_one)

        #Calculate the second ema 
        dataframe = indicators.calculate_ema(dataframe = df, size = ema_two)

        #Free df memory
        del df

        #Calculate the Moving Average Gradients
        dataframe = self.calculate_gradients(
            dataframe = dataframe,
            sma_one = sma_one,
            sma_two = sma_two,
            ema_one = ema_one,
            ema_two = ema_two
        )

        return dataframe

    def calculate_gradients(dataframe, sma_one, sma_two, ema_one, ema_two):
        """
        Function to calculate moving average gradients for the lower and higher SMAs,
        and the moving average gradients for the lower and higher EMAs
        :param dataframe: dataframe object
        :param sma_one: Integer of the lowest timeframe length for SMA
        :param sma_two: Integer of the highest timeframe length for SMA
        :param ema_one: Integer of the lowest timeframe length for EMA
        :param ema_two: Integer of the highest timeframe length for EMA
        :return: dataframe with updated moving average gradients
        """
        
        #Calculate gradient for the lower SMA
        moving_average = "SMA_" + str(sma_one)
        df = indicators.calculate_gradient(dataframe, moving_average)

        #Calculate gradienr for the higher SMA
        moving_average = "SMA_" + str(sma_two)
        df = indicators.calculate_gradient(df, moving_average)

        #Calculate gradient for the lower EMA
        moving_average = "EMA_" + str(ema_one)
        df = indicators.calculate_gradient(df, moving_average)

        #Calculate gradient for the highest EMA
        moving_average = "EMA_" + str(ema_two)
        dataframe = indicators.calculate_gradient(df, moving_average)

        #Free df memory
        del df

        return dataframe

    #Function to determine if a trade event has occurred, and if so, calculate trade signal
    def determine_trade(self, dataframe):
        """
        Function to calculate a trade signal for the strategy. For the Moving Average Gradient Strategy, we apply the following rules:
        1. For a BUY signal, the gradients for the SMAs and EMAs all have to be positive
        2. For a SELL signal, the gradients for the SMAs and EMAs all have to be negative
        

        :param dataframe: dataframe of data with indicators
        :return: dataframe object with trade values added
        """
        dataframe["TRADES"] = "-"

        try:
            for i in range(len(dataframe)):
                ema_two_delta = float(dataframe.iloc[i, (len(dataframe.columns) - 2)])
                ema_one_delta = float(dataframe.iloc[i, (len(dataframe.columns) - 3)])
                sma_two_delta = float(dataframe.iloc[i, (len(dataframe.columns) - 4)])
                sma_one_delta = float(dataframe.iloc[i, (len(dataframe.columns) - 5)])

                moving_averages = [sma_one_delta, sma_two_delta, ema_one_delta, ema_two_delta]

                if self.is_net_positive(moving_averages) & self.has_wide_gradient(moving_averages):
                    dataframe.loc[i, "TRADES"] = "BUY"
                elif self.is_net_negative(moving_averages) & self.has_wide_gradient(moving_averages):
                    dataframe.loc[i, "TRADES"] = "SELL"
                else:
                    dataframe.loc[i, "TRADES"] = "-"

        except KeyError as e:
            print("Dataframe does not contain Moving Average columns")

        return dataframe

    #Function to calculate whether gradient is net_positive
    def is_net_positive(self, moving_averages):
        """
        Function compares each gradient to determine if they are all positive
        :param moving_averages: list of moving averages
        :return: Boolean, True if all gradients are positive 
        """

        #Get lower SMA
        sma_one_delta = moving_averages[0]
        #Get higher SMA
        sma_two_delta = moving_averages[1]
        #Get lower EMA 
        ema_one_delta = moving_averages[2]
        #Get higher EMA
        ema_two_delta = moving_averages[3]
        

        if (sma_one_delta > 0) & (sma_two_delta > 0) & (ema_one_delta > 0) & (ema_two_delta > 0):
            return True
        else:
            return False
        
    #Function to calculate whether gradient is net_negative
    def is_net_negative(self, moving_averages):
        """
        Function compares each gradient to determine if they are all negative
        :param moving_averages: list of moving averages
        :return: Boolean, True if all gradients are negative 
        """

        #Get lower SMA
        sma_one_delta = moving_averages[0]
        #Get higher SMA
        sma_two_delta = moving_averages[1]
        #Get lower EMA 
        ema_one_delta = moving_averages[2]
        #Get higher EMA
        ema_two_delta = moving_averages[3]
        

        if (sma_one_delta < 0) & (sma_two_delta < 0) & (ema_one_delta < 0) & (ema_two_delta < 0):
            return True
        else:
            return False

    #Function to measure the gradients of each Moving Average
    def has_wide_gradient(moving_averages):
        """
        Function to measure the moving average gradient and checks if it is greater than the range
        :param moving_averages: list of moving averages
        :return Boolean: True if the gradients are wider than the range
        """

        #Get lower SMA
        sma_one_delta = abs(moving_averages[0])
        if sma_one_delta < 25:
            return False
        #Get higher SMA
        sma_two_delta = abs(moving_averages[1])
        if sma_two_delta < 25:
            return False
        #Get lower EMA 
        ema_one_delta = abs(moving_averages[2])
        if ema_one_delta < 25:
            return False
        #Get higher EMA
        ema_two_delta = abs(moving_averages[3])
        if ema_two_delta < 25:
            return False


        return True


    