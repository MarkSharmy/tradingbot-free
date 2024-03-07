import pandas as pd
from utils import utils

#Time to wait until next trade {4 = 1Hr}
wait_time = 24 

#Function to simulate Deriv D Trader application
def simulate(data, factor, offset, balance, custom_risk = 0):
    """
    Function to simulate the Deriv DTrader platform. It create a proposal, based on the trade signal.
    If the signal is Rise, the application enters a position expecting the second candle after to close
    above the entry price.
    If the signal is Fall, the application enters a position expecting the second candle after to close
    below the entry price.

    :param data: dataframe object with trade signal
    :return: data object with trade results
    """
    
    
    data = data.copy()
    #Reset the index to numeric default
    data.reset_index(inplace = True)

    #Create a new column called Report to records winnings or losses
    data["Report"] = "Null"

    for i in range(len(data)):
        if i < (len(data) - offset):
            if data.loc[i, "dtrade"] == "Rise":
                data = rise(data, offset, i)
            elif data.loc[i, "dtrade"] == "Fall":
                data = fall(data, offset, i)  

    
    trades = data[data["Report"] != "Null"]
    trades = trades[["time", "dtrade", "Report"]]
    data = calculate_trades(data = trades, balance = balance, factor = factor, custom_risk = custom_risk)  

    return data

def calculate_trades(data, balance, factor, custom_risk):
    #Reset Index for accurate readings
    data.reset_index(inplace = True)
    balance = round(float(balance), 2)
    data["Profit-Loss"] = 0.0

    for i in range(len(data)):
        risk_amount = get_risk_amount(balance, factor, custom_risk)
        if data.loc[i, "Report"] == "Win":
            balance = balance + (risk_amount * 0.95)
            data.loc[i, "Profit-Loss"] = balance
        elif data.loc[i, "Report"] == "Loss":
            balance = balance - risk_amount
            data.loc[i, "Profit-Loss"] = balance
        else:
           data.loc[i, "Profit-Loss"] = balance

    #Set the index back to datime
    data.set_index("time", inplace = True)

    return data

#Function to calculate the amount to risk for a trade
def get_risk_amount(balance, factor, custom_risk = None):
    """
    Function to calculate the amount to risk for a trade, based on the given
    amount of balance
    :param balance: float of account balance
    :return float: amount to risk
    """

    if custom_risk != None:
        return custom_risk
    
    else:
        if balance >= 1400.0:
            return float(factor["1400"])
        elif balance >= 700.0:
            return float(factor["700"])
        elif balance >= 180.0:
            return float(factor["180"])
        elif balance >= 90.0:
            return float(factor["90"])
        elif balance >= 45.0:
            return float(factor["45"])
        elif balance >= 5.0:
            return float(factor["5"])
        elif balance <= 5.0:
            return float(factor["<5"])
        elif balance < 2.0:
            return balance
        else:
            return (balance * 0.10)
        

    

def rise(data, offset, index):
    """
    Function to determine whether price action will rise
    :param data: data object
    :return: data with results
    """
    
    #Entry = open price of the next candle
    entry = data.loc[(index + 1), "open"]

    #Close = close price after the specified offset
    close = data.loc[(index + offset), "close"]

    #If the closing price is higher than the entry price, its a profit
    if close > entry:
        data.loc[index, "Report"] = "Win"
    #If the closing price is less than the entry price, its a loss
    elif close < entry:
        data.loc[index, "Report"] = "Loss"
    #If the closing price is the same as the entry price, then its break even
    else:
        data.loc[index, "Report"] = "Even"

    #Move pointer to wait specified hours to execute the next trade
    utils.pointer = index + wait_time

    return data




def fall(data, offset, index):
    """
    Function to determine whether price action will fall
    :param data: data object
    :return: data with results
    """

    #Entry = open price of the next candle
    entry = data.loc[(index + 1), "open"]

    #Close = close price after the specified offset
    close = data.loc[(index + offset), "close"]

    #If the closing price is less than the entry price, its a profit
    if close < entry:
        data.loc[index, "Report"] = "Win"
    #If the closing price is higher than the entry price, its a loss
    elif close > entry:
        data.loc[index, "Report"] = "Loss"
    #If the closing price is the same as the entry price, then its break even
    else:
        data.loc[index, "Report"] = "Even"

    #Move pointer to wait specified hours to execute the next trade
    utils.pointer = index + wait_time

    return data

#### NOTE: Deprecate
#Function to calculate the offset to determine when to exit trade
def get_offset(exit_time):
    """
    Function to calculate offset
    :param exit_time: string, with the breakout time
    :return int: number of candles to offset
    """

    if exit_time == "30M":
        return 2
    elif exit_time == "45M":
        return 3
    elif exit_time == "1H":
        return 4
    elif exit_time == "2H":
        return 8
    elif exit_time == "3H":
        return 12
    elif exit_time == "4H":
        return 16
    elif exit_time == "5H":
        return 20
    elif exit_time == "6H":
        return 24
    else:
        return 12


