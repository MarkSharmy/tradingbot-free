import time
import tradebot
import deriv_bot
import threading
from user import User
from getpass import getpass
from session import Session
from utils.objects import Point
from utils.enumerations import Trend
from strategies.mm_strategy import MM_Strategy 


#main function {Edit later to allow multiple users to login}
if __name__ == "__main__":  
    
    print("TopTrader Beta Version 0.1.7.1")
    
    broker = input("Choose default broker: [mt5, deriv-drv, deriv-fx, xm, octa]\n")
    broker = broker.lower()

    startup = False
    print("Initiatizing...")

    while startup is False:
        startup = tradebot.start_mt5(broker = broker)

        if startup is False:
            print("Failed. Retrying...")
        else:
            print("Successful")


    accounts = []
    sessions = []

    while 1:

        name = input("Enter name of the account or Q when done: ")

        if name == "Q":

            break

        else:
            #Get Account Information 
            user_name = name
            login = int(input("Enter your MT5 login: "))
            password = getpass("Enter your MT5 password: ")
            server = input("Enter your broker's server: ")
            fill_type = input("Enter fill type: [default, FOK, IOC, RETURN]\n")
            volume = float(input("Enter volume: "))

            #Create User object with account info
            user = User(user_name, login, password, server)

            #Validate account information by loggin into account
            print("Initializing...")

            success = tradebot.initialize(user)
            if success is False:
                print("Failed.")
            else:

                print("Successful")
                #Create an Account object and append to list
                account = dict(user = user, volume = volume, fill = fill_type)
                accounts.append(account) 

    #Log back to default account
    tradebot.start_mt5(broker = broker)

    #Get information on the instrument to trade:
    instrument = input("Enter symbol to trade: ")
    symbol = instrument
    timeframe = input("Enter timeframe: ")

    #Specify trading strategy to trade on the instrument
    strategy = MM_Strategy(symbol)
    timestamp = input("Enter date of peak formation: ")
    strategy.timestamp = timestamp

    #Specify the latest peak on the instrument
    value = float(input("Enter value of peak formation: "))
    strategy.peak = Point(value, timestamp)
    
    #Specify the current trend on the instrument
    trend = input("Enter the market trend [Bull or Bear] : ")

    if trend.lower() == "bull":
        strategy.trend = Trend.BULL

    elif trend.lower() == "bear":
        strategy.trend = Trend.BEAR

    else:
        raise Exception("Invalid market trend")

    #Create Session object and append to list
    sessions.append(Session(accounts, strategy, timeframe))

    #Create a thread for each session
    for session in sessions:
        print("Opening trades for symbol:", session.strategy.symbol)
        threading.Thread(target = session.start).start()

        #print("Symbol", session.strategy.symbol)
        #print("Peak:", session.strategy.peak)
        #print("Trend:", session.strategy.trend)
    

    

    
                

                




