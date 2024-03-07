#### Beta Version
import os
import sys
import asyncio
import requests
from deriv_api import DerivAPI
from deriv_api import APIError

api = None
api_token = None

#Function to initialize global variables
def initialize(account_type, token = None):
    global api
    global api_token

    print("Starting Deriv Trader")

    if token:
        api_token = token
        return

    #Check account type and retrieve the appropriate token from the system's environment variables
    #### NOTE: Environment variables are preset on the local machine. If they are not the program closes

    if account_type.lower() == "demo":
        api_token = os.getenv('DERIV_TOKEN_DEMO', '')
        if len(api_token) == 0:
            sys.exit("DERIV_TOKEN environment variable is not set")

    elif account_type.lower() == "real":
        api_token = os.getenv('DERIV_TOKEN', '')
        if len(api_token) == 0:
            sys.exit("DERIV_TOKEN environment variable is not set")
    else:
        raise KeyError("Invalid account type. Check spelling")
    
    print("API Token:", api_token)
    asyncio.run(authenticate(api_token))



#Function to enter trade on Deriv Trader
async def place_entry(contract_type, symbol, risk_amount):
    """
    Function to place a trade on Deriv Trader
    :param contract_type: String, represting the contract type
    :param symbol: String, deriv specific trade symbol
    :amount: float, amount to risk on a trade
    """
    global api
    global api_token

    ####TODO: Create a variable to hold duration for flexible wait times
    #Initialize api variable
    api = DerivAPI(app_id=1089)

    #await authenticate(api_token)
    balance = await get_account_balance()
    amount = get_risk_amount(balance, risk_amount)

    #Dict object with trade details
    request = {
        "proposal": 1,
               "amount": amount,
               "basis": "stake",
                "contract_type": contract_type,
                "currency": "USD",
                "duration": 60,
                "duration_unit": "s",
                "symbol": symbol
    }

    print("Proposing contract")
    # Get proposal
    proposal = await api.proposal(request)
    #print(proposal)

    print("Buying contract")
    # Buy proposed contract and enter trade
    response = await api.buy({"buy": proposal.get('proposal').get('id'), "price": amount})
    
    if response:
        print("Entry successful")

#Function to authenticate user information from Deriv API
async def authenticate(api_token):
    """
    Function makes a call to Deriv API to authenticate the user token
    :param: String, API token provided by Deriv, retrieved from the env variables
    """
    api = DerivAPI(app_id=1089)
    
    print("Authorizing...")
    authorize = await api.authorize(api_token)

    #Display results to the user
    if authorize:
        print("Authorization successful")
    else:
        print("Authorization failed. Check account details")



#Function to retrieve user account balance
async def get_account_balance():

    #Make call to Deriv API for account balance
    response = await api.balance()
    #Display account balance
    response = response["balance"]
    print("Your current balance is", response['currency'], response['balance'])
    #Convert balance to float type
    balance = float(response["balance"])
    #Return float to caller
    return balance


#Function to calculate the amount to risk for a trade
def get_risk_amount(balance, custom_risk = None):
    """
    Function to calculate the amount to risk for a trade, based on the given
    amount of balance
    :param balance: float of account balance
    :return float: amount to risk
    """
    print("Calculating risk")
    #### TODO: Rewrite the code to work with factor dictionary instead

    if custom_risk != None:
        return custom_risk
    else:
        if balance >= 1400.0:
            return 100.0
        elif balance >= 700.0:
            return 50.0
        elif balance >= 180.0:
            return 20.0
        elif balance >= 90.0:
            return 10.0
        elif balance >= 45.0:
            return 5.0
        elif balance >= 5.0:
            return 2.0
        elif balance <= 5.0:
            return 1.5
        elif balance < 2.0:
            return balance
        else:
            return (balance * 0.10)

#Function to evaluate connection
def is_online():
    return check_connection()


#Function to test the internet connection
def check_connection():

    #Use requests to ping the url and return True is the call was successful
    try:
        response = requests.get("https://www.google.com/", timeout = 5)

        return True
    
    #If exceptionsare raise there is not internet connection and return False
    except requests.exceptions.ReadTimeout:
        return False
    
    except requests.ConnectionError:
        return False
    
    #Catch all exception handler
    except Exception:
        return False
    

#Function to convert order_type to Deriv contract type
def get_deriv_order_type(order_type):

    #### TODO: Convert string order_type to enum object
    #### TODO: Add more contract types to query list
    print("Retrieving contract type")
    if order_type == "Rise":
        return "CALLE"
    elif order_type == "Fall":
        return "PUTE"
    else:
        raise KeyError("Incorrect order type")

#Function to convert MT5 symbols to Deriv API symbols
def get_deriv_symbol(symbol):
    print("Getting deriv symbol")
    #### TODO: Add more symbols to query list
    if symbol == "Volatility 100 Index":
        return "R_100"
    #### TODO: Add more symbols here
    else:
        raise KeyError(f"Unknown symbol: Could not parse {symbol}")
    

def init_trade(candle, symbol, risk_amount):
    """
    Function to evaluate trade signals on a candle
    :param candle: series object with candle data
    :param symbol: string, symbol to trade
    :param factor: dictionary object, with risk management information
    """

    #### NOTE: Pandas boolean expressions are ambigous, solved by bool() function
    print("Deriv Attempting Trade")
    #If BUY signal, order type is Rise
    if (candle["dtrade"] == "Rise").bool():
        contract = get_deriv_order_type("Rise")
        deriv_symbol = get_deriv_symbol(symbol)
        asyncio.run(place_entry(contract_type = contract, symbol = deriv_symbol, risk_amount = risk_amount))
        print("Placed entry at", candle.time, "Rise")

    #If SELL signal, order type is Fall
    elif (candle["dtrade"] == "Fall").bool():
        contract = get_deriv_order_type("Fall")
        deriv_symbol = get_deriv_symbol(symbol)
        asyncio.run(place_entry(contract_type = contract, symbol = deriv_symbol, risk_amount = risk_amount))
        print("Placed entry at", candle.time, "Fall")

    #### TODO: Raise exception here
    else:
        print("Something went wrong on attempt trade")
        pass

    
