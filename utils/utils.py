#Beta Version
import json
import pandas as pd
from utils.enumerations import Gradient

#Function to calculate lot size or volume in MT5
def calculate_volume(balance, risk, stop_loss, stop_price, symbol):
    """
    Function to calculte a lot size (or volume) for a trade on MT5. The balance is passed as a static amount,
    any compounding is taken care of in the parent function.
    :param balance: float of the balance being risked
    :param risk: float of the percentage amount to risk
    :param stop_loss: float of the stop loss
    :param stop_price: float of the entry price
    :param symbol: the symbol as a string
    :return: the lot_size as a float
    """

    #Calculate the amount to risk
    risk_amount = balance * risk

    #Remove any denotation of the symbol
    symbol_name = symbol.split(".")
    symbol = symbol_name[0]

    if symbol == "USDJPY":
        #USDJPY pip size is 0.01
        pip_size = 0.01
        #Calculate the pip value
        pip_value = get_pip_value(
            pip_size = pip_size,
            stop_price = stop_price,
            stop_loss = stop_loss,
            risk_amount = risk_amount
        )
        #Calculate the raw lot_size
        raw_lot_size = pip_value / 1000
    else:
        pip_size = 0.0001
        #Calculate the pip value
        pip_value = get_pip_value(
            pip_size = pip_size,
            stop_price = stop_price,
            stop_loss = stop_loss,
            risk_amount = risk_amount
        )
        #Calculate the raw lot_size
        raw_lot_size = pip_value / 10

    #Format lot size to be MT5 friendly. This may change based on the broker (i.e. if they do micro lots etc)
    lot_size = float(raw_lot_size)
    #Round to 2 decimal places. NOTE: If you have a small balance (< 5000 USD) this rounding may imapct risk
    lot_size = round(lot_size, 2)

    #A quick catch to make sure lot size isn't extreme. You can modify this
    if lot_size >= 10:
        lot_size = 9.99
    
    return lot_size

def get_pip_value(pip_size, stop_price, stop_loss, risk_amount):
    #Calculate the amount of pips being risked
    pips_gained = abs((stop_price - stop_loss) / pip_size)
    #Calculate the pip value
    pip_value = risk_amount / pips_gained
    #Add in exchange rate as the USD is the counter currency
    pip_value = pip_value * stop_price


#Function to save a json object to file
def save_json(dict):
    """
    Function saves the latest peak candle as a json object to file: peak.json
    :param json: dictionary object with the candle information
    :return: Boolean, true is save was successful
    """

    try:
        json_obj = json.dumps(dict)

        with open("peak.json", "w") as outfile:
            outfile.write(json_obj)

            return True
        
    except Exception as e:
        print("An IO Error has occurred. Save unsuccessful")
        return False

    

#Function to calculate the gradient of a indicator
def calculate_gradient(dataframe, symbol, indicator, period):
    """
    Function to calculate the gradient of a indicator. Moving average can be an EMA or SMA.
    The gradient is measure from the point 3 candles before the most recent average. If the gradient
    is positive, the indicator is a bullish trend, otherwise if the gradient is negative, the
    indicator is a bearish trend.
    :param dataframe: the dataframe to be analyzed
    :param indicator:  string of the indicator column
    :return: dataframe with the indicator gradients
    """

    column_name = indicator + "_Delta"

    dataframe[column_name] = 0.00

    divider = get_divider(symbol = symbol)

    #Loop through each row and calculate the gradient of the Moving Average
    for i in range(len(dataframe)):
        #If the index is less than 3 init delta to 0.00
        if i < 3: 
            dataframe.loc[i, column_name] = 0.00
        #Else find the gradient between the MAs of the last 4 candles 
        else:
            #m2 = most recent candles
            m2 = dataframe.loc[i, indicator]
            #m1 = 3 candles from the most recent candle
            m1 = dataframe.loc[(i - period), indicator]
            #Apply the gradient formula
            delta = (m2 - m1) / divider
            #Round delta to 1 decimal place
            delta = round(delta, 1)
            #Add the calculated gradient to the row
            dataframe.loc[i, column_name] = delta

    return dataframe

#Function to test gradient 
def test_gradient(delta, type):

    if type == Gradient.NEGATIVE:
        return (delta < 0) #& (delta > -100)
    elif type == Gradient.POSITIVE:
        return (delta > 0) #& (delta > 250)
    else:
        raise KeyError("Incorrect input value on test_gradient() function")
    

def calculate_cross(dataframe: pd.DataFrame, indicator_1: str, indicator_2: str) -> pd.DataFrame:
    """
    :return: dataframe with cross events
    """

    #Get the column names

    #column 1
    column_one = indicator_1
    #column 2
    column_two = indicator_2

    
    #Position column i.e differences between ema_one and ema_two
    try:
        dataframe["Pos"] = dataframe[column_one] - dataframe[column_two]

    except KeyError as e:
        print("KeyError: EMA columns undefined")

    
    #Pre-position column with the previous positions
    dataframe["Pre_Pos"] = dataframe["Pos"].shift(1)
    
    dataframe.dropna()

    column_name = "tdi_cross"
    
    #Define the crossover events
    dataframe[column_name] = dataframe.apply(is_cross, axis = 1)
 
    #Drop the position and pre-position columns
    dataframe.drop(columns = ["Pos", "Pre_Pos"], inplace = True)

    return dataframe

#Function to apply to series data for cross calculate
def is_cross(candle):
    """
    Function to apply to each candle of a dataframe to determine if a cross event has occurred
    :param candle: series object, candle from a dataframe
    """

    if candle.Pos >= 0 and candle.Pre_Pos < 0:
        return 1
    elif candle.Pos <= 0 and candle.Pre_Pos > 0:
        return -1
    else:
        return 0


#### TODO: Complete function to calculate divider for each symbol
def get_divider(symbol :str) -> float:
    #### NOTE: Add more symbols

    if symbol == "EURCAD":
        return 0.0001
    
    elif symbol == "EURCHF":
        return 0.0001

    elif symbol == "EURGBP":
        return 0.0001

    elif symbol == "EURJPY":
        return 0.01

    elif symbol == "EURUSD":
        return 0.0001

    elif symbol == "GBPCAD":
        return 0.0001

    elif symbol == "GBPJPY":
        return 0.01
    
    elif symbol == "CADJPY":
        return 0.01

    elif symbol == "GBPUSD":
        return 0.0001

    elif symbol == "NZDCAD":
        return 0.0001

    elif symbol == "NZDJPY":
        return 0.01

    elif symbol == "USDCAD":
        return 0.0001
    
    elif symbol == "EURCAD":
        return 0.0001

    elif symbol == "USDCHF":
        return 0.0001

    elif symbol == "USDJPY":
        return 0.01

    elif symbol == "OILCash":
        return 0.1

    elif symbol == "BTCUSD":
        return 10.0
    
    elif symbol == "ETHUSD":
        return 10.0

    elif symbol == "XAUUSD":
        return 1.0

    elif symbol == "XAUEUR":
        return 0.01

    elif symbol == "Volatility 100 Index":
        return 1.0

    else:
        raise Exception("Unknown Trading Symbol")
    

def get_sl_value(symbol):
    
    if symbol == "EURCAD":
        return 0.0025
    
    elif symbol == "EURCHF":
        return 0.0025
    
    elif symbol == "EURGBP":
        return 0.0025
    
    elif symbol == "EURJPY":
        return 0.25
    
    elif symbol == "EURUSD":
        return 0.0025
    
    elif symbol == "GBPCAD":
        return 0.0025
    
    elif symbol == "GBPJPY":
        return 0.25
    
    elif symbol == "CADJPY":
        return 0.25
    
    elif symbol == "GBPUSD":
        return 0.0025
    
    elif symbol == "NZDCAD":
        return 0.0025
    
    elif symbol == "NZDJPY":
        return 0.25
    
    elif symbol == "USDCAD":
        return 0.0025
    
    elif symbol == "EURCAD":
        return 0.0025
    
    elif symbol == "USDCHF":
        return 0.0025
    
    elif symbol == "USDJPY":
        return 0.25
    
    elif symbol == "OILCash":
        return 2.5
    
    elif symbol == "BTCUSD":
        return 250.0
    
    elif symbol == "ETHUSD":
        return 250.0
    
    elif symbol == "XAUUSD":
        return 25.0
    
    elif symbol == "XAUEUR":
        return 0.25
    
    elif symbol == "Volatility 100 Index":
        return 50.0

    else:
        raise Exception("Unknown Trading Symbol")

def get_br_value(symbol):
    
    if symbol == "EURCAD":
        return 0.0025
    
    elif symbol == "EURCHF":
        return 0.0025
    
    elif symbol == "EURGBP":
        return 0.0025
    
    elif symbol == "EURJPY":
        return 0.25
    
    elif symbol == "EURUSD":
        return 0.0025
    
    elif symbol == "GBPCAD":
        return 0.0025
    
    elif symbol == "GBPJPY":
        return 0.25
    
    elif symbol == "CADJPY":
        return 0.25
    
    elif symbol == "GBPUSD":
        return 0.0025
    
    elif symbol == "NZDCAD":
        return 0.0025
    
    elif symbol == "NZDJPY":
        return 0.25
    
    elif symbol == "USDCAD":
        return 0.0025
    
    elif symbol == "EURCAD":
        return 0.0025
    
    elif symbol == "USDCHF":
        return 0.0025
    
    elif symbol == "USDJPY":
        return 0.25
    
    elif symbol == "OILCash":
        return 2.5
    
    elif symbol == "BTCUSD":
        return 250.0
    
    elif symbol == "ETHUSD":
        return 250.0
    
    elif symbol == "XAUUSD":
        return 25.0
    
    elif symbol == "XAUEUR":
        return 0.25
    
    elif symbol == "Volatility 100 Index":
        return 50.0

    else:
        raise Exception("Unknown Trading Symbol")

def get_tp_value(symbol):
    
    if symbol == "EURCAD":
        return 0.005
    
    elif symbol == "EURCHF":
        return 0.005
    
    elif symbol == "EURGBP":
        return 0.005
    
    elif symbol == "EURJPY":
        return 0.5
    
    elif symbol == "EURUSD":
        return 0.005
    
    elif symbol == "GBPCAD":
        return 0.005
    
    elif symbol == "GBPJPY":
        return 0.5
    
    elif symbol == "CADJPY":
        return 0.5
    
    elif symbol == "GBPUSD":
        return 0.005
    
    elif symbol == "NZDCAD":
        return 0.005
    
    elif symbol == "NZDJPY":
        return 0.5
    
    elif symbol == "USDCAD":
        return 0.005
    
    elif symbol == "EURCAD":
        return 0.005
    
    elif symbol == "USDCHF":
        return 0.005
    
    elif symbol == "USDJPY":
        return 0.5
    
    elif symbol == "OILCash":
        return 5.0
    
    elif symbol == "BTCUSD":
        return 500.0
    
    elif symbol == "ETHUSD":
        return 500.0
    
    elif symbol == "XAUUSD":
        return 50.0
    
    elif symbol == "XAUEUR":
        return 0.5
    
    elif symbol == "Volatility 100 Index":
        return 50.0

    else:
        raise Exception("Unknown Trading Symbol")

def round_for_symbol(symbol):

    if symbol == "EURCAD":
        return 5
    
    elif symbol == "EURCHF":
        return 5
    
    elif symbol == "EURGBP":
        return 5
    
    elif symbol == "EURJPY":
        return 3
    
    elif symbol == "EURUSD":
        return 5
    
    elif symbol == "GBPCAD":
        return 5
    
    elif symbol == "GBPJPY":
        return 3
    
    elif symbol == "CADJPY":
        return 3
    
    elif symbol == "GBPUSD":
        return 5
    
    elif symbol == "NZDCAD":
        return 5
    
    elif symbol == "NZDJPY":
        return 3
    
    elif symbol == "USDCAD":
        return 5
    
    elif symbol == "EURCAD":
        return 5
    
    elif symbol == "USDCHF":
        return 5
    
    elif symbol == "USDJPY":
        return 3
    
    elif symbol == "OILCash":
        return 2
    
    elif symbol == "BTCUSD":
        return 1
    
    elif symbol == "ETHUSD":
        return 1
    
    elif symbol == "XAUUSD":
        return 1
    
    elif symbol == "XAUEUR":
        return 3
    
    elif symbol == "Volatility 100 Index":
        return 2

    else:
        raise Exception("Unknown Trading Symbol")


     






