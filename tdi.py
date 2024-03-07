import numpy as np
import pandas as pd
from utils import utils

#TDI Super Class
class TDI():

    #Instance Variables
    @property
    def peak(self):
        return self.__peak
    
    @peak.setter
    def peak(self, value):
        self.__peak = value

    @property
    def trough(self):
        return self.__trough
    
    @trough.setter
    def trough(self, value):
        self.__trough = value

    @property
    def highest(self):
        return self.__highest
    
    @highest.setter
    def highest(self, value):
        self.__highest = value

    @property 
    def lowest(self):
        return self.__lowest
    
    @lowest.setter
    def lowest(self, value):
        self.__lowest = value

    #Constructor
    def __init__(self):

        self.__peak = 0
        self.__trough = 0
        self.__highest = 0
        self.__lowest = 0

    def update_range(self, data, indicator_column, period, num_candles):
        """
        Function to update highest and lowest values for the given range
        :param data: dataframe object
        :param indicator_column: string, column name of the indicator
        :param period: int period of the indicator
        :param num_candles: integer, number of candles to analyze
        :return: void
        """

        #Grab n number of candles from the dataframe, where n = num_candles
        data = data[-num_candles:]

        #Reset index for new dataframe
        data.reset_index(inplace = True)

        #Initialize highest and lowest instance variables
        self.highest = 0

        if data.loc[0, indicator_column] == 0:
            self.lowest = data.loc[period, indicator_column]
        else:
            self.lowest = data.loc[0, indicator_column]


        #Update Values
        data[indicator_column].apply(self.cast)

        #Get offset for the given symbol
        #offset = self.get_offset(symbol)

        self.peak = self.highest 
        self.trough = self.lowest


    #Function to update highest and lowest positions
    def cast(self, indicator_value):

        if indicator_value == 0.0:
            #Invalid value
            pass

        elif indicator_value > self.highest:
            self.highest = indicator_value

        elif indicator_value < self.lowest:
            self.lowest = indicator_value

        else:
            #No change
            pass

    #Function to calculate the value of the indicator on the TDI scale
    def get_value(self, current_value):

        range = self.get_range()
        pos = current_value - self.trough
        percentile = round((pos / range) * 100)

        return percentile
    
    #Get the maximum value on the TDI scale
    def get_maximum(self):

        range = self.get_range()
        #Get value at 70% mark
        max = self.trough + (0.7 * range)

        return max

    #Get the minimum value on the TDI scale
    def get_minimum(self):
        
        range = self.get_range()
        #Get value at 20% mark
        min = self.trough + (0.2 * range)

        return min

    #Function to calculate the range between highest and lowest peaks
    def get_range(self):

        #The difference between the highest and lowest points
        difference = self.peak - self.trough
        #The size of 1 unit = 1/10 of the difference between the highest and lowest points
        unit = difference / 10.0
        #Adjusted range for scale, 1 unit above the peak and 1 unit below the trough
        range = (2 * unit) + difference
        #Adjust the Trough by 1 unit for more accurate readings
        self.trough = self.trough - unit

        return range
    
    #Function to calculate cross between two indicators
    def calculate_cross(self, dataframe, indicator_1, indicator_2):
        """
        Function to calculate cross between two different indicators on the TDI scale
        :param indicator_1: String, column name of the first indicator
        :param indicator_2: String, column name of the second indicator
        return: int, 0 - no cross | 1 - cross above | -1 - cross below
        """

        #Position column i.e. diffrences between indicator 1 and indicator 2

        try:
            dataframe["Pos"] = dataframe[indicator_1] - dataframe[indicator_2]

        except KeyError as e:
            print("KeyError: Indicator Columns not specified")

        #Pre-position column with the previous positions
        dataframe["Pre_Pos"] = dataframe["Pos"].shift(1)

        dataframe["Pre_Pos"].fillna(0)

        #Define the crossover events
        dataframe["tdi_cross"] = dataframe.apply(self.func_0919p, axis = 1)

        #Drop the position and pre-position columns
        dataframe = dataframe.drop(columns = ["Pos", "Pre_Pos"])

        return dataframe
    
    
    #Function to apply to series data frame cross calculation
    def func_0919p(self, candle):
        
        if candle.Pos >= 0 and candle.Pre_Pos < 0:
            return 1
        elif candle.Pos <= 0 and candle.Pre_Pos > 0:
            return -1
        else:
            return 0


#Bollinger TDI indicator class
class Bollinger():

    #Instance Variables
    @property
    def peak(self):
        return self.__peak
    
    @peak.setter
    def peak(self, value):
        self.__peak = value

    @property
    def trough(self):
        return self.__trough
    
    @trough.setter
    def trough(self, value):
        self.__trough = value

    @property
    def highest(self):
        return self.__highest
    
    @highest.setter
    def highest(self, value):
        self.__highest = value

    @property 
    def lowest(self):
        return self.__lowest
    
    @lowest.setter
    def lowest(self, value):
        self.__lowest = value

    #Constructor
    def __init__(self):

        self.__peak = 0
        self.__trough = 0
        self.__highest = 0
        self.__lowest = 0

    def update_range(self, data, period, num_candles):
        """
        Function to update highest and lowest values for Bollinger values within a shared range
        :param data: dataframe object
        :param period: int period of the indicator
        :param num_candles: integer, number of candles to analyze
        :return: void
        """

        #Grab n number of candles from the dataframe, where n = num_candles
        data = data[-num_candles:]

        #Reset index for new dataframe
        data.reset_index(inplace = True)

        #Initialize highest and lowest instance variables
        self.highest = 0

        if data.loc[0, "Lower"] == 0:
            self.lowest = data.loc[period, "Lower"]
        else:
            self.lowest = data.loc[0, "Lower"]


        #Update Values
        data.apply(self.cast, axis = 1)

        self.peak = self.highest 
        self.trough = self.lowest



    #Function to update highest and lowest positions
    def cast(self, candle):

        lower = candle["Lower"]
        upper = candle["Upper"]

        if lower == 0.0:
            #Invalid value
            pass

        elif upper > self.highest:
            self.highest = upper

        elif lower < self.lowest:
            self.lowest = lower

        else:
            #No change
            pass



    #Function to calculate the value of the indicator on the TDI scale
    def get_value(self, current_value):

        range = self.get_range()
        pos = current_value - self.trough
        percentile = round((pos / range) * 100)

        return percentile
    
    #Get the maximum value on the TDI scale
    def get_maximum(self):

        range = self.get_range()
        #Get value at 70% mark
        max = self.trough + (0.7 * range)

        return max

    #Get the minimum value on the TDI scale
    def get_minimum(self):
        
        range = self.get_range()
        #Get value at 20% mark
        min = self.trough + (0.2 * range)

        return min

    #Function to calculate the range between highest and lowest peaks
    def get_range(self):

        #The difference between the highest and lowest points
        difference = self.peak - self.trough
        #The size of 1 unit = 1/10 of the difference between the highest and lowest points
        unit = difference / 10.0
        #Adjusted range for scale, 1 unit above the peak and 1 unit below the trough
        range = (2 * unit) + difference
        #Adjust the Trough by 1 unit for more accurate readings
        self.trough = self.trough - (0.7 * unit)

        return range
    
    #Function to calculate cross between two indicators
    def calculate_cross(self, dataframe, indicator_1, indicator_2):
        """
        Function to calculate cross between two different indicators on the TDI scale
        :param indicator_1: String, column name of the first indicator
        :param indicator_2: String, column name of the second indicator
        return: int, 0 - no cross | 1 - cross above | -1 - cross below
        """

        #Position column i.e. diffrences between indicator 1 and indicator 2

        try:
            dataframe["Pos"] = dataframe[indicator_1] - dataframe[indicator_2]

        except KeyError as e:
            print("KeyError: Indicator Columns not specified")

        #Pre-position column with the previous positions
        dataframe["Pre_Pos"] = dataframe["Pos"].shift(1)

        dataframe["Pre_Pos"].fillna(0)

        #Define the crossover events
        dataframe["tdi_cross"] = dataframe.apply(self.func_0919p, axis = 1)

        #Drop the position and pre-position columns
        dataframe = dataframe.drop(columns = ["Pos", "Pre_Pos"])

        return dataframe
    
    
    #Function to apply to series data frame cross calculation
    def func_0919p(self, candle):
        
        if candle.Pos >= 0 and candle.Pre_Pos < 0:
            return 1
        elif candle.Pos <= 0 and candle.Pre_Pos > 0:
            return -1
        else:
            return 0
