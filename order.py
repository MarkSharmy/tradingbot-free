
import tradebot
import pandas as pd
from user import User
from utils import utils
from utils import logger
import MetaTrader5 as mt5
from utils.enumerations import *


class Order():

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
    def comment(self):
        return self.__comment
    
    @comment.setter
    def comment(self, comment: str):
        self.__comment = comment


    #Constructor
    def __init__(self, symbol, user):
        self.symbol = symbol
        self.user = user

    def initialize_user(self) -> bool:

        success = False

        while success is False:
            success = tradebot.initialize(self.user)

            if success is False:
                print("Failed. Retrying...")
            else:
                print("Successful")

        return success


    #Function to place an order on MetaTrader 5
    def place_order(self, symbol, order_type, fill_type, price, stop_loss, take_profit, volume, comment, direct = False):
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
        request["type_filling"] = fill_type
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
                    fill_type = fill_type,
                    price = price, 
                    stop_loss = stop_loss,
                    take_profit = take_profit,
                    volume = volume,
                    comment = comment,
                    direct = True
                )

            else:
                logger.log_error(result[0], symbol)

    #Function to create an order on MetaTrader 5
    def create_order(self, signal: str, volume: float, filling: Order_Filling):
        """
        Function to define order details for a position on MetaTrader 5.
        This is where stop loss and take profit params are defined.
        #NOTE: Order type and Order action can be added on later versions
        :param symbol: String, symbol for the currency pair
        :param candle: Series object, which candle information, with the signal
        :return void: #NOTE: for now.
        """

        candle = tradebot.get_candlesticks(symbol = self.symbol, timeframe = "M15", limit = 1)

        print("Signal:", signal)

        if signal == "BUY":
            stop_loss = utils.get_sl_value(self.symbol)
            take_profit = utils.get_tp_value(self.symbol)
            decimal_places = utils.round_for_symbol(self.symbol)
            current_price = float(candle["close"])
            price = mt5.symbol_info_tick(self.symbol).ask
            sl_price = float(round((current_price - stop_loss), decimal_places))
            tp_price = float(round((current_price + take_profit), decimal_places))
            comment = "BUY ORDER 008"
            order_type = mt5.ORDER_TYPE_BUY #TODO: Modify this later, to accept different order types
            fill_type = self.get_order_filling(filling)

        elif signal == "SELL":
            stop_loss = utils.get_sl_value(self.symbol)
            take_profit = utils.get_tp_value(self.symbol)
            decimal_places = utils.round_for_symbol(self.symbol)
            current_price = float(candle["close"])
            price = mt5.symbol_info_tick(self.symbol).bid
            sl_price = float(round((current_price + stop_loss), decimal_places))
            tp_price = float(round((current_price - take_profit), decimal_places))
            comment = "SELL ORDER 008"
            order_type = mt5.ORDER_TYPE_SELL #TODO: Modify this later, to accept different order types
            fill_type = self.get_order_filling(filling)

        #TODO: Modify this function later to accept custom Order types and Order actions later
        self.place_order(
            symbol = self.symbol,
            order_type = order_type,
            fill_type = fill_type,
            price = price,
            stop_loss = sl_price,
            take_profit = tp_price,
            volume = volume,
            comment = comment
        )

    #Function to trail stop loss
    def trail_stop_loss(self):
        pass

    #Function to cancel an order on MT5
    def cancel_order(self):
        """
        Function to cancel an order indentified by an order number
        :param order_number: integer representing the order number from MT5
        :return: Boolean, True == cancelled, False == not cancelled.
        """

        order_number = self.ticket
        
        #Create the request
        request = {
            "action": mt5.TRADE_ACTION_REMOVE,
            "order": order_number,
            "comment": "Order Removed"
        }

        try:
            order_result = mt5.order_send(request)
            if order_result[0] == 10009:
                print(f"Order {order_number} succussfully cancelled")
                return True
            #### TODO: Add custom error handling
            else:
                print(f"Order {order_number} unable to cancel")
                return False
        except Exception as e:
            print(f"An error occurred whilst trying to cancel order {order_number}")
            raise Exception("Check cancel_order function")
        
    
    #Function to return all currently open orders on MetaTrader 5
    @staticmethod
    def get_all_open_orders():
        """
        Function to retrieve all open orders from MetaTrader 5
        :return: list of open orders
        """
        return mt5.orders_get()

    def get_order_type(self, order_type: str) -> str:
    
        if order_type.lower() == 'buy':
            return mt5.ORDER_TYPE_BUY
        
        elif order_type.lower() == 'buy_limit':
            return mt5.ORDER_TYPE_BUY_LIMIT
        
        elif order_type.lower() == 'buy_stop':
            return mt5.ORDER_TYPE_BUY_STOP
        
        elif order_type.lower() == 'buy_stop_limit':
            return mt5.ORDER_TYPE_BUY_STOP_LIMIT
        
        elif order_type.lower() == 'sell':
            return mt5.ORDER_TYPE_SELL
        
        elif order_type.lower() == 'sell_limit':
            return mt5.ORDER_TYPE_SELL_LIMIT
        
        elif order_type.lower() == 'sell_stop':
            return mt5.ORDER_TYPE_SELL_STOP
        
        elif order_type.lower() == 'sell_stop_limit':
            return mt5.ORDER_TYPE_SELL_STOP_LIMIT
        
        elif order_type.lower() == "close_by":
            return mt5.ORDER_TYPE_CLOSE_BY
        
        else:
            raise Exception("Invalid Order Type. Check source code: Function -> get_order_type()")


    def get_order_action(self, order_action: Order_Action):
    
        if order_action == Order_Action.DEAL:
            return mt5.TRADE_ACTION_DEAL
        
        elif order_action == Order_Action.MODIFY:
            return mt5.TRADE_ACTION_MODIFY
        
        elif order_action == Order_Action.PENDING:
            return mt5.TRADE_ACTION_PENDING
        
        elif order_action == Order_Action.REMOVE:
            return mt5.TRADE_ACTION_REMOVE
        
        elif order_action == Order_Action.SLTP:
            return mt5.TRADE_ACTION_SLTP
        
        elif order_action == Order_Action.CLOSE_BY:
            return mt5.TRADE_ACTION_CLOSE_BY
        
        else:
            raise Exception("Invalid Order Action. Check source code: Function -> get_order_action()")
        


    def get_order_filling(self, order_filling: Order_Filling):

        if order_filling == Order_Filling.FOK:
            return mt5.ORDER_FILLING_FOK
        
        elif order_filling == Order_Filling.IOC:
            return mt5.ORDER_FILLING_IOC
        
        elif order_filling == Order_Filling.BOC:
            return mt5.ORDER_FILLING_BOC
        
        elif order_filling == Order_Filling.RETURN:
            return mt5.ORDER_FILLING_RETURN
        
        else:
            raise Exception("Invalid Oder Action. Check source code: Function -> get_order_filling()")