import deriv_bot
import tradebot
from session import Dtrader
from strategies.tt_strategy import TT_Strategy

print("Botch Trader V-0.1.2")

account = input("Dev or Client account: ")

if account.lower() == "dev":

    account_type = input("Demo or Real: ")

    deriv_bot.initialize(account_type)
    
    startup = False
    print("Initiatizing...")

    while startup is False:
        startup = tradebot.start_mt5(broker = "deriv-drv")

        if startup is False:
            print("Failed. Retrying...")
        else:
            print("Successful")

    risk_amount = float(input("Enter risk amount: "))

    strategy = TT_Strategy(symbol = "Volatility 100 Index")
    
    dtrader = Dtrader(strategy = strategy, risk_amount = risk_amount)

    dtrader.start()

elif account.lower() == "client":

    token = input("Enter API token: ")
    
    deriv_bot.initialize(account_type = "Null", token = token)

    startup = False
    print("Initiatizing...")

    while startup is False:
        startup = tradebot.start_mt5(broker = "deriv-drv")

        if startup is False:
            print("Failed. Retrying...")
        else:
            print("Successful")

    risk_amount = float(input("Enter risk amount: "))

    strategy = TT_Strategy(symbol = "Volatility 100 Index")
    
    dtrader = Dtrader(strategy = strategy, risk_amount = risk_amount)

    dtrader.start()

else:
    raise Exception("Please enter the correct account type!")