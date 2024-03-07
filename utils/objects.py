import pandas as pd
from utils.enumerations import Trend
from utils import utils

class Point(object):

    @property
    def timestamp(self):
        return self.__timestamp
    
    @timestamp.setter
    def timestamp(self, time):
        self.__timestamp = time

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        self.__value = value

    #Constructor
    def __init__(self, value = 0.0, timestamp = "2000-01-01 00:00:00"):
        self.__timestamp = timestamp
        self.__value = value

    def __str__(self) -> str:
        return "Price: " + str(self.value) + ", @ " + str(self.timestamp)

    def __repr__(self) -> str:
        return "Price: " + str(self.value) + ", @ " + str(self.timestamp)
            


class Setup():

    @property
    def symbol(self) -> str:
        return self.__symbol

    @symbol.setter
    def symbol(self, symbol: str):
        self.__symbol = symbol

    @property
    def first_leg(self) -> pd.Series:
        return self.__first_leg

    @first_leg.setter
    def first_leg(self, first_leg):
        self.__first_leg = first_leg

    @property
    def apex(self) -> pd.Series:
        return self.__apex
    
    @apex.setter
    def apex(self, apex):
        self.__apex = apex

    @property
    def second_leg(self) -> pd.Series:
        return self.__second_leg

    @second_leg.setter
    def second_leg(self, second_leg):
        self.__second_leg = second_leg

    @property
    def signal_candle(self) -> pd.Series:
        return self.__signal_candle
    
    @signal_candle.setter
    def signal_candle(self, candle):
        self.__signal_candle = candle

    @property
    def has_signal(self) -> bool:
        return self.__has_signal
    
    @has_signal.setter
    def has_signal(self, flag: bool):
        self.__has_signal = flag


    #Constructor
    def __init__(self, symbol: str, entry_leg):
        self.first_leg = 0
        self.second_leg = 0
        self.bull_points = 0
        self.bear_points = 0
        self.count = 0
        self.apex = 0
        self.has_signal = False
        self.signal_candle = 0
        self.symbol = symbol
        self.add_first_leg(entry_leg)
        

    def add_first_leg(self, candle):
        self.first_leg = candle
        self.bear_points = 1
        self.bull_point = 1


    def check_signal(self, trend: Trend, closing_candle: pd.Series, starting_candle: pd.Series):

        if trend == Trend.BEAR:

            try:
                pip_value = closing_candle.high - self.first_leg.high
                distance = abs(round(pip_value / utils.get_divider(self.symbol)))
                
                pip_value = self.apex.low - self.first_leg.high
                height = abs(round(pip_value / utils.get_divider(self.symbol)))

                delta = abs(round(closing_candle["upper_tdi"] - starting_candle["upper_tdi"]))
                channel = round(closing_candle["upper_tdi"] - closing_candle["lower_tdi"])

                if(channel >= 15) & (delta <= 5) & (distance <= 16):
                    self.signal_candle = closing_candle
                    self.has_signal = True

            except:
                self.has_signal = False

        if trend == Trend.BULL:

            try:
                pip_value = self.second_leg.low - self.first_leg.low
                distance = abs(round(pip_value / utils.get_divider(self.symbol)))
                
                pip_value = self.apex.high - self.first_leg.low
                height = abs(round(pip_value / utils.get_divider(self.symbol)))

                delta = abs(round(closing_candle["lower_tdi"] - starting_candle["lower_tdi"]))
                channel = round(closing_candle["upper_tdi"] - closing_candle["lower_tdi"])

                if(channel >= 15) & (delta <= 5) & (distance <= 16):
                    self.signal_candle = closing_candle
                    
                    self.has_signal = True

            except:
                self.has_signal = False

    def is_complete(self) -> bool:

        if isinstance(self.first_leg, int):

            return False
        
        if isinstance(self.second_leg, int):

            return False
        
        if isinstance(self.apex, int):

            return False
        
        return True

    
    def update(self, dataframe: pd.DataFrame, candle: pd.Series, start_index: int):

        trend = candle.trend

        rsi_line = int(candle["rsi"])

        signal_line = int(candle["signal_line"])


        if (candle["signal_cross"] != 0):
            self.count += 1


        if trend == Trend.BEAR:


            if (rsi_line < signal_line) & (self.bear_points <= 2):

                if isinstance(self.apex, int):
                    self.apex = candle

                else:
                    if candle.low < self.apex.low:
                        self.apex = candle
                
                self.bear_points = 2

            if (rsi_line > signal_line) & (self.bear_points <= 3):

                if isinstance(self.second_leg, int):
                    self.second_leg = candle

                else:
                    if candle.high > self.second_leg.high:
                        self.second_leg = candle

                self.bear_points = 3

            if (rsi_line < signal_line) & (self.bear_points == 3):

                diff = signal_line - rsi_line
                if diff >= 2:
                    self.bear_points = 4
                    self.check_signal(
                        trend = trend,
                        closing_candle = candle,
                        starting_candle = dataframe.loc[start_index]
                        )
                else:
                    self.bear_points = 0

        if trend == Trend.BULL:

            if (rsi_line > signal_line) & (self.bull_points <= 2):

                if isinstance(self.apex, int):
                    self.apex = candle

                else:
                    if candle.high > self.apex.high:
                        self.apex = candle
                
                self.bull_points = 2

            if (rsi_line < signal_line) & (self.bull_points <= 3):

                if isinstance(self.second_leg, int):
                    self.second_leg = candle

                else:
                    if candle.low < self.second_leg.low:
                        self.second_leg = candle

                self.bull_points = 3

            if (rsi_line > signal_line) & (self.bull_points == 3):

                diff = rsi_line - signal_line
                if diff >= 2:
                    self.bull_points = 4
                    self.check_signal(
                        trend = trend,
                        closing_candle = candle,
                        starting_candle = dataframe.loc[start_index]
                        )
                else:
                    self.bull_points = 0



class MiniSetup():

    @property
    def symbol(self) -> str:
        return self.__symbol

    @symbol.setter
    def symbol(self, symbol: str):
        self.__symbol = symbol

    @property
    def first_leg(self) -> pd.Series:
        return self.__first_leg

    @first_leg.setter
    def first_leg(self, first_leg):
        self.__first_leg = first_leg

    @property
    def apex(self) -> pd.Series:
        return self.__apex
    
    @apex.setter
    def apex(self, apex):
        self.__apex = apex

    @property
    def second_leg(self) -> pd.Series:
        return self.__second_leg

    @second_leg.setter
    def second_leg(self, second_leg):
        self.__second_leg = second_leg

    @property
    def signal_candle(self) -> pd.Series:
        return self.__signal_candle
    
    @signal_candle.setter
    def signal_candle(self, candle):
        self.__signal_candle = candle

    @property
    def has_signal(self) -> bool:
        return self.__has_signal
    
    @has_signal.setter
    def has_signal(self, flag: bool):
        self.__has_signal = flag


    #Constructor
    def __init__(self, symbol: str, entry_leg):
        self.first_leg = 0
        self.second_leg = 0
        self.bull_points = 0
        self.bear_points = 0
        self.count = 0
        self.apex = 0
        self.has_signal = False
        self.signal_candle = 0
        self.symbol = symbol
        self.add_first_leg(entry_leg)
        

    def add_first_leg(self, candle):
        self.first_leg = candle
        self.bear_points = 1
        self.bull_point = 1


    def check_signal(self, trend: Trend, closing_candle: pd.Series, starting_candle: pd.Series):

        if trend == Trend.BEAR:

            try:
                pip_value = closing_candle.high - self.first_leg.high
                distance = abs(round(pip_value / utils.get_divider(self.symbol)))
                
                pip_value = self.apex.low - self.first_leg.high
                height = abs(round(pip_value / utils.get_divider(self.symbol)))

                delta = abs(round(closing_candle["upper_tdi"] - starting_candle["upper_tdi"]))
                channel = round(closing_candle["upper_tdi"] - closing_candle["lower_tdi"])

                if(channel >= 15) & (delta <= 5) & (distance <= 16):
                    self.signal_candle = closing_candle
                    self.has_signal = True

            except:
                self.has_signal = False

        if trend == Trend.BULL:

            try:
                pip_value = self.second_leg.low - self.first_leg.low
                distance = abs(round(pip_value / utils.get_divider(self.symbol)))
                
                pip_value = self.apex.high - self.first_leg.low
                height = abs(round(pip_value / utils.get_divider(self.symbol)))

                delta = abs(round(closing_candle["lower_tdi"] - starting_candle["lower_tdi"]))
                channel = round(closing_candle["upper_tdi"] - closing_candle["lower_tdi"])

                if(channel >= 10) & (distance <= 10):
                    self.signal_candle = closing_candle
                    
                    self.has_signal = True

            except:
                self.has_signal = False

    def is_complete(self) -> bool:

        if isinstance(self.first_leg, int):

            return False
        
        if isinstance(self.second_leg, int):

            return False
        
        if isinstance(self.apex, int):

            return False
        
        return True

    
    def update(self, dataframe: pd.DataFrame, candle: pd.Series, start_index: int, trend: Trend):


        rsi_line = int(candle["rsi"])

        signal_line = int(candle["signal_line"])


        if (candle["signal_cross"] != 0):
            self.count += 1


        if trend == Trend.BEAR:


            if (rsi_line < signal_line) & (self.bear_points <= 2):

                if isinstance(self.apex, int):
                    self.apex = candle

                else:
                    if candle.low < self.apex.low:
                        self.apex = candle
                
                self.bear_points = 2

            if (rsi_line > signal_line) & (self.bear_points <= 3):

                if isinstance(self.second_leg, int):
                    self.second_leg = candle

                else:
                    if candle.high > self.second_leg.high:
                        self.second_leg = candle

                self.bear_points = 3

            if (rsi_line < signal_line) & (self.bear_points == 3):

                diff = signal_line - rsi_line
                if diff >= 2:
                    self.bear_points = 4
                    self.check_signal(
                        trend = trend,
                        closing_candle = candle,
                        starting_candle = dataframe.loc[start_index]
                        )
                else:
                    self.bear_points = 0

        if trend == Trend.BULL:

            if (rsi_line > signal_line) & (self.bull_points <= 2):

                if isinstance(self.apex, int):
                    self.apex = candle

                else:
                    if candle.high > self.apex.high:
                        self.apex = candle
                
                self.bull_points = 2

            if (rsi_line < signal_line) & (self.bull_points <= 3):

                if isinstance(self.second_leg, int):
                    self.second_leg = candle

                else:
                    if candle.low < self.second_leg.low:
                        self.second_leg = candle

                self.bull_points = 3

            if (rsi_line > signal_line) & (self.bull_points == 3):

                diff = rsi_line - signal_line
                if diff >= 2:
                    self.bull_points = 4
                    self.check_signal(
                        trend = trend,
                        closing_candle = candle,
                        starting_candle = dataframe.loc[start_index]
                        )
                else:
                    self.bull_points = 0


        

        


            

    

    