import datetime as dt
from datetime import date, datetime

#Function to retrieve hour time stamp
def round_hour(time):
    time_string = str(time)
    chars = list(time_string)
    chars[14] = "0"
    chars[15] = "0"

    result = "".join(chars)
    return result 

#Function to retrive the date of from a candle
def get_date_string(time):
    time.date()
    time_string = str(time)
    chars = list(time_string)
    chars = chars[:10]
    day = "".join(chars)
    day = date.fromisoformat(day)
    day = str(day)
    return day

#Function to convert datetime string to datetime object
def to_datetime(datetime_string):
    """
    Function to covert datetime string to datetime object
    :param time_string: string or TimeStamp, datetime as a string
    :return: datetime object
    """
    
    format = "%Y-%m-%d %H:%M:%S"
    converted_string = str(datetime_string)
    dateobj = datetime.strptime(converted_string, format)

    return dateobj

#Function to determine whether candle is within asian range
def in_asian_range(time):

    start = dt.time(23, 0, 0)
    end = dt.time(23, 59, 59)
    
    asian_start = dt.time(0, 0, 0)
    asian_end = dt.time(7, 0, 0)
    
    current_datetime = to_datetime(time)
    current_time = current_datetime.time()


    night_range  = start <= current_time <= end 
    asian_range = asian_start <= current_time <= asian_end 

    if night_range:

        return True
    
    elif asian_range:

        return True
    
    else:

        return False