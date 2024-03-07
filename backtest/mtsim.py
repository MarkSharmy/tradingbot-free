import pandas as pd
from utils import utils

#Function to simulate trades on MetaTrader
def simulate_dep(dataframe, symbol, lot_size, balance):

    dataframe["GAINS"] = 0.0
    dataframe["Profit-Loss"] = 0.0

    for i in range(len(dataframe)):

        #Test signal for a Bearish Trend
        if dataframe.loc[i, "SIGNALS"] == "SELL":

            index  = i + 1
            current_price = dataframe.loc[index, "open"]
            highest_price = 0.0
            lowest_price = current_price

            stop_loss = round(current_price + 0.002, 5)
            sl_flag = False

            take_profit_1 = round(current_price - 0.002, 5)
            tp_flag_1 = False

            data = dataframe.loc[i:]
            data.reset_index(inplace = True)

            count = 0
            for j in range(len(data)):
                
                if((data.loc[j, "high"] >= stop_loss) & (~tp_flag_1)):

                    sl_flag = True
                    highest_price = stop_loss
                    break

                if(data.loc[j, "low"] <= take_profit_1):

                    tp_flag_1 = True
                    lowest_price = take_profit_1

                else:
                    continue

            if sl_flag:
                
                distance = current_price - highest_price
                divider = utils.get_divider(symbol)
                pips = round((distance / divider), 1)
                dataframe.loc[i, "GAINS"] = pips

            elif tp_flag_1:
                distance = current_price - lowest_price
                divider = utils.get_divider(symbol)
                pips = round((distance / divider), 1)
                dataframe.loc[i, "GAINS"] = pips

            else:
                continue

        elif dataframe.loc[i, "SIGNALS"] == "BUY":

            index  = i + 1
            current_price = dataframe.loc[index, "open"]
            lowest_price = 0.0
            highest_price = current_price

            stop_loss = round(current_price - 0.0025, 5)
            sl_flag = False

            take_profit_1 = round(current_price + 0.005, 5)
            tp_flag_1 = False

            data = dataframe.loc[i:]
            data.reset_index(inplace = True)

            count = 0
            for j in range(len(data)):
                
                if((data.loc[j, "low"] <= stop_loss) & (~tp_flag_1)):

                    sl_flag = True
                    lowest_price = stop_loss
                    break

                if(data.loc[j, "high"] >= take_profit_1):

                    tp_flag_1 = True
                    highest_price = take_profit_1

                else:
                    continue

            if sl_flag:
                
                distance = lowest_price - current_price
                divider = utils.get_divider(symbol)
                pips = round((distance / divider), 1)
                dataframe.loc[i, "GAINS"] = pips

            elif tp_flag_1:
                distance = highest_price - current_price
                divider = utils.get_divider(symbol)
                pips = round((distance / divider), 1)
                dataframe.loc[i, "GAINS"] = pips

            else:
                continue

        
        else:
            #No Signal
            continue

        
    
    trades = dataframe[["time", "SIGNALS", "GAINS", "Profit-Loss"]]
    trades.reset_index(inplace = True)

    for i in range(len(trades)):

        gain = round(((10 * lot_size) * trades.loc[i, "GAINS"]), 2)
        new_balance = balance + gain
        trades.loc[i, "Profit-Loss"] = new_balance
        balance = new_balance


    return trades


def calculate_gains(dataframe: pd.DataFrame, symbol: str, order_type: str):

    sl = utils.get_sl_value(symbol)

    dataframe.reset_index(inplace = True)
    current_price = dataframe.loc[0, "open"]

    if order_type == "BUY":

        sl_price = current_price - sl

        for i in range(len(dataframe)):

            rsi = round(dataframe.loc[i, "rsi"])
            closing_price = dataframe.loc[i, "close"]

            if (dataframe.loc[i, "low"]) <= sl_price:

                return -25.0
            
            if rsi > 60:

                stop_price = dataframe.loc[i, "close"]
                distance = stop_price - current_price
                gains = round(distance / utils.get_divider(symbol), 2)

                return gains
            

                

            
            if closing_price < current_price:

                stop_price = dataframe.loc[i, "close"]
                distance = stop_price - current_price
                gains = round(distance / utils.get_divider(symbol), 2)

                return gains
            
            else:
                continue
            


    elif order_type == "SELL":

        sl_price = current_price + sl

        for i in range(len(dataframe)):

            rsi = round(dataframe.loc[i, "rsi"])
            closing_price = dataframe.loc[i, "close"]

            if (dataframe.loc[i, "high"]) >= sl_price:

                return -25.0
            
            if rsi < 39:

                stop_price = dataframe.loc[i, "close"]
                distance = current_price - stop_price
                gains = round(distance / utils.get_divider(symbol), 2)

                return gains
            
                
            
            if closing_price > current_price:

                stop_price = dataframe.loc[i, "close"]
                distance = current_price - stop_price
                gains = round(distance / utils.get_divider(symbol), 2)

                return gains
            
                
            
            

    else:
        raise Exception("SOME KIND OF ERROR")




#Function to simulate trades on MetaTrader
def simulate(dataframe: pd.DataFrame, symbol: str, lot_size: float, balance: float) -> pd.DataFrame:

    #Column for all gains and losses
    dataframe["GAINS"] = 0.0
    #Column for current balance
    dataframe["Account_Balance"] = 0.0

    dataframe["SYMBOL"] = symbol

    # 1:1 distances for each trail
    distances = [25, 20, 20, 10]
    pips = 0.0
    count = 0

    for i in range(len(dataframe)):

        if dataframe.loc[i, "SIGNALS"] != "-":

            #Get index of the signal
            position = i
            #Flag binding to to start loop
            winning = True

            while(winning):
                
                #If price still trailing reset count to 3 for 10 pips
                if count > 3:
                    count = 3

                #Trail stop loss
                winning, position = trail_sl(
                    dataframe = dataframe[position + 1:],
                    distance = distances[count],
                    symbol = symbol,
                    order_type = dataframe.loc[i, "SIGNALS"]
                )

                if winning:

                    pips += distances[count]
                    count += 1

                else:

                    pips -= distances[count]
                    count = 0

            dataframe.loc[i, "GAINS"] = pips
            pips = 0
            

        else:
            #No signal
            continue 


    trades = dataframe[["time", "SYMBOL", "SIGNALS", "GAINS", "Account_Balance"]]
    trades.reset_index(inplace = True)

    for i in range(len(trades)):

        gain = round(((10 * lot_size) * trades.loc[i, "GAINS"]), 2)
        new_balance = balance + gain
        trades.loc[i, "Account_Balance"] = new_balance
        balance = new_balance


    return trades

#Function to simulate trading stop loss
def trail_sl(dataframe: pd.DataFrame , distance: int, symbol: str, order_type: str):
     
     
    #Create a column to store all the original indexes
    dataframe["index"] = dataframe.index
    #Reset index for accurate looping 
    dataframe.reset_index(inplace = True)

    #Calculate stop loss
    sl = distance * utils.get_divider(symbol)
    #Calculate take profit
    tp = distance * utils.get_divider(symbol)


    current_price = dataframe.loc[0, "open"]

    #Flag for stop loss
    sl_flag = False
    #Flag for take profit
    tp_flag = False
    #position to be returned
    index = 0

    if order_type == "BUY":

        sl_price = current_price - sl
        tp_price = current_price + tp 

        for i in range(len(dataframe)):
            
            #If the candle lowest price is less than or equal to stop loss, and TP isnt flagged
            #flag SL and break out of loop
            if ((dataframe.loc[i, "low"] <= sl_price) & (~tp_flag)):

                sl_flag = True    
                break
            
            #If candle highest price is greater or equal to take profit, flagged TP
            if (dataframe.loc[i, "high"] >= tp_price):

                tp_flag = True
                #Retrieve the index of the candle to return to caller
                index = dataframe.loc[i, "index"]
                #break out of loop, to save comp time
                break

    elif order_type == "SELL":

        sl_price = current_price + sl
        tp_price = current_price - tp 

        for i in range(len(dataframe)):
            index = dataframe.loc[i, "index"]
            #If the candle highest price is greater than or equal to stop loss, and TP isnt flagged
            #flag SL and break out of loop
            if ((dataframe.loc[i, "high"] >= sl_price) & (~tp_flag)):

                sl_flag = True
                break
            
            #If candle lowest price is less or equal to take profit, flagged TP
            if (dataframe.loc[i, "low"] <= tp_price):

                tp_flag = True
                #Retrieve the index of the candle to return to caller
                index = dataframe.loc[i, "index"]
                #break out of loop, to save comp time
                break

    else:
        raise Exception("Invalid Order Type!")
    
    """///////////////////////END OF TRAILING//////////////////////////"""



    if sl_flag & ~tp_flag:
        return  False, 0
    
    elif tp_flag:
        return True, index
    
    else:
        print("Index:", index)
        return False, 0
        #raise Exception("Something wrong with the logic")
        
        