#Beta Version

import json
from user import User
import pandas as pd
import MetaTrader5 as mt5
from datetime import datetime

#Function to start MT5 from User object
def initialize(user: User) -> bool:
    """
    Function to start MetaTrader 5 from json file
    :param user: User object with user login, password, server, file location
    :return: Boolean, True if started successfully, or False if it fails to start
    """

    user_info = dict(login = user.login, password = user.password, server = user.server, path = user.path)

    #Ensure that all variables are set/formatted to the correct type
    username = user_info["login"]
    login = int(username)
    password = user_info["password"]
    server = user_info["server"]
    path = user_info["path"]
    timeframe = "M1"

    #Attempt to initialize MT5
    mt_init = False
    
    try:
        
        mt_init = mt5.initialize(
            path = path,
            login = login, 
            password = password,
            server = server,
            timeframe = timeframe,
            portable = False
        )

    #Handle any errors
    except Exception as e:
        print(f"Error initializing MetaTrader : {e}")
        mt_init = False

    mt_login = False

    if mt_init:

        try:
            mt_login = mt5.login(
                login = login,
                password = password,
                server = server
            )

        except Exception as e:
            print(f"Error logging into MetaTrader 5: {e}")

    if mt_login:
        return True
    
    return False


#Function to start MT5 from json
def start_mt5(broker = "xm"):
    """
    Function to start MetaTrader 5 from json file
    :param user: json object with user login, password, server, file location
    :param broker: string, with the broker key to initialize with
    :return: Boolean, True if started successfully, or False if it fails to start
    """

    user = User.get_user(broker)

    #Ensure that all variables are set/formatted to the correct type
    username = user["login"]
    login = int(username)
    password = user["password"]
    server = user["server"]
    path = user["path"]
    timeframe = user["timeframe"]

    #Attempt to initialize MT5
    mt_init = False
    
    try:
        
        mt_init = mt5.initialize(
            path = path,
            login = login, 
            password = password,
            server = server,
            timeframe = timeframe,
            portable = False
        )

    #Handle any errors
    except Exception as e:
        print(f"Error initializing MetaTrader : {e}")
        mt_init = False

    mt_login = False

    if mt_init:

        try:
            mt_login = mt5.login(
                login = login,
                password = password,
                server = server
            )

        except Exception as e:
            print(f"Error logging into MetaTrader 5: {e}")

    if mt_login:
        return True
    
    return False

def initialize_symbol(symbol = "EURUSD"):
    symbols = mt5.symbols_get()
    symbol_names = []

    for s in symbols:
        symbol_names.append(s.name)

    if symbol in symbol_names:
        try:
            mt5.symbol_select(symbol, True)
            return True
        except Exception as e:
            print(f"Error in selecting {symbol}. Error: {e}")
            return False
        
    else:
        print(f"Symbol {symbol} does not exist")
        return False

def get_candlesticks(symbol, timeframe, offset = 1, limit = 5000):

    if limit > 50000:
        raise ValueError("No more than 50,000 candles allowed")
    
    timeframe = set_query_timeframe(timeframe)

    candles = mt5.copy_rates_from_pos(symbol, timeframe, offset, limit)
    dFrame = pd.DataFrame(candles)
    candles = pd.DataFrame(dFrame)
    candles.time = pd.to_datetime(candles.time, unit = "s")
    
    return candles

def get_candlesticks_range(symbol, timeframe, startdate, enddate):

    format = "%Y-%m-%d"

    date_from = datetime.strptime(startdate, format)
    date_to = datetime.strptime(enddate, format)
    
    timeframe = set_query_timeframe(timeframe)

    candles = mt5.copy_rates_range(symbol, timeframe, date_from, date_to)
    
    dFrame = pd.DataFrame(candles)
    candles = pd.DataFrame(dFrame)
    candles.time = pd.to_datetime(candles.time, unit = "s")
    return candles


def get_current_time(symbol, timeframe):
    """
    Function to extract the current time for the specified timeframe
    for a given symbol
    :param symbol: string of the symbol to be traded
    :param timeframe: string of the timeframe
    :return: current time
    """
    
    latest_candle = get_candlesticks(symbol = symbol, timeframe = timeframe, limit = 1)
    current_time = latest_candle["time"][0]
    return current_time

def set_query_timeframe(timeframe):
    
    if timeframe == "M1":
        return mt5.TIMEFRAME_M1
    elif timeframe == "M5":
        return mt5.TIMEFRAME_M5
    elif timeframe == "M10":
        return mt5.TIMEFRAME_M10
    elif timeframe == "M15":
        return mt5.TIMEFRAME_M15
    elif timeframe == "M30":
        return mt5.TIMEFRAME_M30
    elif timeframe == "H1":
        return mt5.TIMEFRAME_H1
    elif timeframe == "H4":
        return mt5.TIMEFRAME_H4
    elif timeframe == "D1":
        return mt5.TIMEFRAME_D1
    else:
        raise ValueError(f"Timeframe {timeframe} not supported")


if __name__ == "__main__":
    pass