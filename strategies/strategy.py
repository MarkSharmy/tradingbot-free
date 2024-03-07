#Beta Version

import tradebot

class Strategy(object):


    def __init__(self):
        pass

    def test(self, dataframe, symbol):
        pass

    def run(self, dataframe, symbol):
        pass

    def retrieve_candle_data(self, symbol, timeframe, limit, offset = 1):
        """
        Function to retrieve data from MT5. Data is in the form of candlesticks and is retrieved as a dataframe
        :param symbol: string of the symbol to be retrieved
        :param timeframe: string of the timeframe to retrieved
        :return: dataframe of data
        """

        candles = tradebot.get_candlesticks(symbol = symbol, timeframe = timeframe, offset = offset, limit = limit)

        return candles


        
