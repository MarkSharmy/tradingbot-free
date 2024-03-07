#Beta Version

from enum import Enum, auto

class Trend(Enum):
    BULL = auto()
    RESET_BULL = auto()
    BEAR = auto()
    RESET_BEAR = auto()
    RESET = auto()
    NULL = auto()

    def opposite(self):

        if self == Trend.BULL:

            return Trend.BEAR
        

        elif self == Trend.BEAR:
            
            return Trend.BULL



class Contract(Enum):
    RISE = auto()
    FALL = auto()

class Gradient(Enum):
    POSITIVE = auto()
    NEGATIVE = auto()

class Levels(Enum):
    LEVEL_1 = auto()
    LEVEL_2 = auto()
    LEVEL_3 = auto()
    UNDEFINED = auto()

    def increment(self):

        if self == Levels.UNDEFINED:
            return Levels.LEVEL_1

        elif self == Levels.LEVEL_1:
            return Levels.LEVEL_2

        elif self == Levels.LEVEL_2:
            return Levels.LEVEL_3

        elif self == Levels.LEVEL_3:
            return Levels.UNDEFINED

class MA(Enum):
    SMA = auto()
    EMA = auto()

class Timeframe(Enum):
    M1 = auto()
    M5 = auto()
    M15 = auto()
    M30 = auto()
    H1 = auto()
    H4 = auto()
    D1 = auto()
    W1 = auto()

class Order_Type(Enum):
    BUY = auto()
    SELL = auto()
    BUY_LIMIT = auto()
    SELL_LIMIT = auto()
    BUY_STOP = auto()
    SELL_STOP = auto()
    BUY_STOP_LIMIT = auto()
    SELL_STOP_LIMIT = auto()
    CLOSE_BY = auto()

class Order_Action(Enum):
    DEAL = auto()
    PENDING = auto()
    SLTP = auto()
    MODIFY = auto()
    REMOVE = auto()
    CLOSE_BY = auto()

class Order_Filling(Enum):
    BOC = auto()
    FOK = auto()
    IOC = auto()
    RETURN = auto()

class Order_Time(Enum):
    GTC = auto()
    DAY = auto()
    SPECIFIED = auto()
    SPECIFIED_DAY = auto()


