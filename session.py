import time
import warnings
import tradebot
import deriv_bot
import pandas as pd
from order import Order
from scalp import Scalp
from utils.enumerations import Order_Filling
from strategies.strategy import Strategy


class Session():

    @property
    def symbol(self):
        return self.__symbol

    @symbol.setter
    def symbol(self, symbol: str):
        self.__symbol = symbol

    @property
    def strategy(self):
        return self.__strategy
    
    @strategy.setter
    def strategy(self, strategy: Strategy):
        self.__strategy = strategy

    @property
    def timeframe(self):
        return self.__timeframe
    
    @timeframe.setter
    def timeframe(self, timeframe: str):
        self.__timeframe = timeframe


    @property
    def accounts(self):
        return self.__accounts
    
    @accounts.setter
    def accounts(self, accounts):

        self.__accounts = accounts


    #Constructor 
    def __init__(self, accounts, strategy, timeframe):

        self.accounts = accounts
        self.strategy = strategy
        self.symbol = strategy.symbol
        self.timeframe = timeframe 


    def start(self):
        pass

        print("Session starting:")

        current_time = 0
        prev_time = 0

        while 1:


            #Get value for current time
            current_time = tradebot.get_current_time(symbol = self.symbol, timeframe = self.timeframe)

            #If current time and previous time are not the same a new candle has occurred
            if current_time != prev_time:

                #Run strategy and get latest signal
                candle = self.run_strategy()
                print(self.symbol)
                print(candle)
                
                if self.has_signal(candle):

                    if (candle["SIGNALS"] == "BUY").bool():
                        signal = "BUY"

                    elif (candle["SIGNALS"] == "SELL").bool():
                        signal = "SELL"

                    #Create order and place it on MT5 for each user
                    for account in self.accounts:

                        user = account["user"]
                        print("fill:", account["fill"])
                        volume = account["volume"]
                        print("Volume:", volume)
                        fill_type = self.get_fill_type(account["fill"])

                        new_order = Order(self.symbol, user)
                        new_order.create_order(signal = signal, volume = volume, filling = fill_type)

                    #tradebot.start_mt5()

                #Reset candle time
                prev_time = current_time

            else:
                time.sleep(1)

            time.sleep(1)
     

    #Function to evaluate trade signal
    def has_signal(self, candle):
        """
        Function to evaluate if the candle has a trade signal
        :param: Series object with candle data
        :return: Boolean, returns True if candle has a signal other than '-'
        """
        print("Checking signal")
        #Check SIGNALS column for BUY or SELL signal
        if (candle["SIGNALS"] != "-").bool():
            print("True")
            #return True if it has either BUY or SELL
            return True
        else:
            #Otherwise return False
            print("False")
            return False

    #Function to run a Trading Strategy that tracks trade events
    def run_strategy(self):
        """
        Function to evaluate candle data and runs a Trading Strategy to produce trading signals.
        :param strategy: strategy, Strategy object to run on candle data
        :return candle: Series object with signal event
        """

        #This function supresses warnings and stops them from being logged to the console
        warnings.simplefilter(action='ignore', category=FutureWarning)

        #This function suppress warning messages about pandas using copy-view
        pd.options.mode.chained_assignment = None

        #run() function returns the lastest candle data
        candle, candles = self.strategy.run()

        #Return the lastest candle to the caller as a series object
        return candle
    
    #Function to determine fill type
    def get_fill_type(self, type: str):
        
        if type.lower() == "default":
            return Order_Filling.FOK
        
        if type.lower() == "fok":
            return Order_Filling.FOK
        
        if type.lower() == "ioc":
            return Order_Filling.IOC
        
        if type.lower() == "boc":
            return Order_Filling.BOK
        
        if type.lower() == "return":
            return Order_Filling.RETURN

        raise Exception("Invaid Filling Type: Check spelling")
    
class Scalper():

    @property
    def symbol(self):
        return self.__symbol

    @symbol.setter
    def symbol(self, symbol: str):
        self.__symbol = symbol

    @property
    def strategy(self):
        return self.__strategy
    
    @strategy.setter
    def strategy(self, strategy: Strategy):
        self.__strategy = strategy

    @property
    def timeframe(self):
        return self.__timeframe
    
    @timeframe.setter
    def timeframe(self, timeframe: str):
        self.__timeframe = timeframe

    @property
    def dtrade(self):
        return self.__dtrade

    @property
    def volume(self):
        return self.__volume
    
    @volume.setter
    def volume(self, volume: float):
        self.__volume = volume

    @property
    def users(self):
        return self.__users
    
    @users.setter
    def users(self, users):

        self.__users = users


    #Constructor 
    def __init__(self, users, strategy, timeframe, volume):

        self.users = users
        self.strategy = strategy
        self.symbol = strategy.symbol
        self.timeframe = timeframe 
        self.volume = volume


    def start(self):
        pass

        print("Session starting:")

        current_time = 0
        prev_time = 0

        while 1:


            #Get value for current time
            current_time = tradebot.get_current_time(symbol = self.symbol, timeframe = self.timeframe)

            #If current time and previous time are not the same a new candle has occurred
            if current_time != prev_time:

                #Run strategy and get latest signal
                candle = self.run_strategy()
                print(self.symbol)
                print(candle)
                
                if self.has_signal(candle):

                    if (candle["SIGNALS"] == "BUY").bool():
                        signal = "BUY"

                    elif (candle["SIGNALS"] == "SELL").bool():
                        signal = "SELL"

                    #Create order and place it on MT5 for each user
                    for user in self.users:
                        scalp = Scalp(self.symbol, user)
                        scalp.create_order(signal = signal, volume = self.volume)

                for scalp in self.scalps:
                    scalp.update(candle)

                #Reset candle time
                prev_time = current_time

            else:
                time.sleep(1)

            time.sleep(1)
     

    #Function to evaluate trade signal
    def has_signal(self, candle):
        """
        Function to evaluate if the candle has a trade signal
        :param: Series object with candle data
        :return: Boolean, returns True if candle has a signal other than '-'
        """
        print("Checking signal")
        #Check SIGNALS column for BUY or SELL signal
        if (candle["SIGNALS"] != "-").bool():
            print("True")
            #return True if it has either BUY or SELL
            return True
        else:
            #Otherwise return False
            print("False")
            return False

    #Function to run a Trading Strategy that tracks trade events
    def run_strategy(self):
        """
        Function to evaluate candle data and runs a Trading Strategy to produce trading signals.
        :param strategy: strategy, Strategy object to run on candle data
        :return candle: Series object with signal event
        """

        #This function supresses warnings and stops them from being logged to the console
        warnings.simplefilter(action='ignore', category=FutureWarning)

        #This function suppress warning messages about pandas using copy-view
        pd.options.mode.chained_assignment = None

        #run() function returns the lastest candle data
        candle, candles = self.strategy.run()

        #Return the lastest candle to the caller as a series object
        return candle

class Dtrader():

    @property
    def symbol(self):
        return self.__symbol

    @symbol.setter
    def symbol(self, symbol: str):
        self.__symbol = symbol

    @property
    def strategy(self):
        return self.__strategy
    
    @strategy.setter
    def strategy(self, strategy: Strategy):
        self.__strategy = strategy

    @property
    def risk_amount(self) -> float:
        return self.__risk_amount
    
    @risk_amount.setter
    def risk_amount(self, amount: float):
        self.__risk_amount = amount


    #Constructor 
    def __init__(self, strategy, risk_amount):

        self.strategy = strategy
        self.symbol = strategy.symbol
        self.risk_amount = risk_amount


    def start(self):
        pass

        print("Session starting:")

        current_time = 0
        prev_time = 0

        while 1:


            #Get value for current time
            current_time = tradebot.get_current_time(symbol = self.symbol, timeframe = "M1")

            #If current time and previous time are not the same a new candle has occurred
            if current_time != prev_time:

                #Run strategy and get latest signal
                candle = self.run_strategy()
                print(self.symbol)
                print(candle)
                
                if self.has_signal(candle):
                    deriv_bot.init_trade(candle, self.symbol, self.risk_amount)    

                #Reset candle time
                prev_time = current_time

            else:
                time.sleep(1)

            time.sleep(1)
     

    #Function to evaluate trade signal
    def has_signal(self, candle):
        """
        Function to evaluate if the candle has a trade signal
        :param: Series object with candle data
        :return: Boolean, returns True if candle has a signal other than '-'
        """
        print("Checking signal")
        #Check SIGNALS column for BUY or SELL signal
        if (candle["dtrade"] != "-").bool():
            print("True")
            #return True if it has either BUY or SELL
            return True
        else:
            #Otherwise return False
            print("False")
            return False

    #Function to run a Trading Strategy that tracks trade events
    def run_strategy(self):
        """
        Function to evaluate candle data and runs a Trading Strategy to produce trading signals.
        :param strategy: strategy, Strategy object to run on candle data
        :return candle: Series object with signal event
        """

        #This function supresses warnings and stops them from being logged to the console
        warnings.simplefilter(action='ignore', category=FutureWarning)

        #This function suppress warning messages about pandas using copy-view
        pd.options.mode.chained_assignment = None

        #run() function returns the lastest candle data
        candle = self.strategy.run()

        #Return the lastest candle to the caller as a series object
        return candle


