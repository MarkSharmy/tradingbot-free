import tradebot
import pandas as pd
from user import User
from utils import utils
from utils import logger
import MetaTrader5 as mt5
from utils.enumerations import *

class Scalp():

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, user):
        self.__user = user

    @property
    def symbol(self):
        return self.__symbol
    
    @symbol.setter
    def symbol(self, symbol: str):
        self.__symbol = symbol

    @property
    def ticket(self):
        return self.__ticket
    
    @ticket.setter
    def ticket(self, ticket):
        self.__ticket = ticket

    @property
    def entry_price(self) -> pd.Series:
        return self.__entry_price
    
    @entry_price.setter
    def entry_price(self, candle: pd.Series):
        self.__entry_price = candle

    #Constructor
    def __init__(self, symbol, user):
        self.symbol = symbol
        self.user = user

    def initialize_user(self) -> bool:

        user_info = dict(login = self.user.login, password = self.user.password, server = self.user.server, path = self.user.path)
        success = False

        while success is False:
            success = tradebot.initialize(user_info)

            if success is False:
                print("Failed. Retrying...")
            else:
                print("Successful")

        return success
    
    #Function to create an order on MetaTrader 5
    def create_order(self, signal: str, volume: float):
        """
        Function to define order details for a position on MetaTrader 5.
        This is where stop loss and take profit params are defined.
        #NOTE: Order type and Order action can be added on later versions
        :param symbol: String, symbol for the currency pair
        :param candle: Series object, which candle information, with the signal
        :return void: #NOTE: for now.
        """

        candle = tradebot.get_candlesticks(symbol = self.symbol, timeframe = "M15", limit = 1)
        self.entry_price = candle

        if signal == "BUY":
            stop_loss = 100.0
            take_profit = 90.0
            current_price = float(candle["close"])
            price = mt5.symbol_info_tick(self.symbol).ask
            sl_price = float(round((current_price - stop_loss), 2))
            tp_price = float(round((current_price + take_profit), 2))
            comment = "Scalp Sniper"
            order_type = mt5.ORDER_TYPE_BUY #TODO: Modify this later, to accept different order types

        elif signal == "SELL":
            stop_loss = 100.0
            take_profit = 90.0
            current_price = float(candle["close"])
            price = mt5.symbol_info_tick(self.symbol).bid
            sl_price = float(round((current_price + stop_loss), 2))
            tp_price = float(round((current_price - take_profit), 2))
            comment = "Scalp Sniper"
            order_type = mt5.ORDER_TYPE_SELL #TODO: Modify this later, to accept different order types

        #TODO: Modify this function later to accept custom Order types and Order actions later
        self.place_order(
            symbol = self.symbol,
            order_type = order_type,
            price = price,
            stop_loss = sl_price,
            take_profit = tp_price,
            volume = volume,
            comment = comment
        )

    #Function to place an order on MetaTrader 5
    def place_order(self, symbol, order_type, price, stop_loss, take_profit, volume, comment, direct = False):
        """
        Function to place an order on MetaTrader 5. Function checks the order first (best practice), then places trade if
        order check returns True
        
        """

        #Initialize account on MT5 to execute trade
        print("Initializing account for:", self.user.name)
        startup = self.initialize_user()

        if startup:   
            print("Successful.")

        else:
            print("failed!")


        #Set up order request as a dictionary object. This will be the request sent to MT5
        request = {
            "symbol": symbol,
            "price": price,
            "sl": stop_loss,
            "tp": take_profit, 
            "volume": volume,
            "type_time": mt5.ORDER_TIME_GTC,
            "comment": comment
        }


        #Update the request
        request["type"] = order_type
        request["type_filling"] = mt5.ORDER_FILLING_FOK
        request["action"] = mt5.TRADE_ACTION_DEAL

        

        #If direct is True, go straight ahead to adding the order
        if direct:
            #Send the order to MT5 Terminal
            order_result = mt5.order_send(request)
            print(order_result)

            
            #Notify based on the return outcomes
            if order_result[0] == 10009:
                print(f"Order for {symbol} successful")
                print("Ticket:", order_result[2])
                self.ticket = order_result[2]
                
            else:
                logger.log_error(order_result[0], symbol)
                

        else:
            #Check the order
            result = mt5.order_check(request)

            #If the check passes send the order
            if result[0] == 0:

                print(f"Order check for {symbol} was successful. Placing order")
                
                #Place order recursively
                self.place_order(
                    symbol = symbol,
                    order_type = order_type,
                    price = price, 
                    stop_loss = stop_loss,
                    take_profit = take_profit,
                    volume = volume,
                    comment = comment,
                    direct = True
                )

            else:
                logger.log_error(result[0], symbol)


    #Function to update the current scalp order
    def update(self, candle: pd.Series):
        print("Entry price:", self.entry_price.close)
        print("Current Price:", candle.close)

    #Function to cancel an order on MT5
    def close_order(self):
        """
        Function to cancel an order indentified by an order number
        :param order_number: integer representing the order number from MT5
        :return: Boolean, True == cancelled, False == not cancelled.
        """

        comment = "Closed order for ticket: " + str(self.ticket)

        mt5.Close(symbol = self.symbol, ticket = self.ticket)
        
        print(comment)