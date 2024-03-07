
#Function to log error message from MT5 error codes
def log_error(code: int, symbol: str):

    if code == 10004:
        print(f"Error: Tried to requote the same order for {symbol}")

    elif code == 10006:
        print(f"Error: Request rejected!")

    elif code == 10007:
        print(f"Error: Order request was canceled by trader")

    elif code == 10008:
        print(f"Error: Order was already placed")

    elif code == 10010:
        print(f"Error: Only part of the request could be completed for {symbol}")

    elif code == 10011:
        print(f"Error occurred during processing for {symbol}")

    elif code == 10012:
        print(f"Error: Request canceled by timeout")

    elif code == 10013:
        print(f"Error: request is invalid for {symbol}")

    elif code == 10014:
        print(f"Error: Invalid volume for {symbol}")

    elif code == 10015:
        print(f"Error: Invalid price for {symbol}")

    elif code == 10016:
        print(f"Error: Invalid stop loss and take profit for {symbol}")

    elif code == 10017:
        print(f"Error: Trading is disabled")

    elif code == 10018:
        print(f"Error: Market is closed")

    elif code == 10019:
        print(f"Error: Insuffient funds")

    elif code == 10020:
        print(f"Error: Priced changed for {symbol}")

    elif code == 10021:
        print(f"Error: There are no quotes to process the request for {symbol}")

    elif code == 10022:
        print(f"Error: Invalid order, expiration date in the request")

    elif code == 10023:
        print(f"Error: Order state changed")

    elif code == 10024:
        print(f"Error: Too many requests")

    elif code == 10025:
        print(f"Error: No changes in request")

    elif code == 10026:
        print(f"Error: Autotrading disabled by server")

    elif code == 10027:
        print(f"Error: Autotrading disabled by client terminal")

    elif code == 10028:
        print(f"Error: Request locked for processing")

    elif code == 10029:
        print(f"Error: Order or position frozen")

    elif code == 10030:
        print(f"Error: Invalid filling type for {symbol}")

    elif code == 10031:
        print(f"Connection Error")

    elif code == 10032:
        print(f"Error: Operation is only allowed for live accounts")

    elif code == 10033:
        print(f"The number of pending orders has reached the limit")

    elif code == 10034:
        print(f"The volume of orders and positions for {symbol} has reached the limit")

    elif code == 10035:
        print(f"Error: Incorrect or prohibited order type for {symbol}")

    elif code == 10036:
        print(f"Error: Position has been closed")

    elif code == 10038:
        print(f"Error: Close volume exceeds the current position volume")

    elif code == 10039:
        print(f"Error: A close order already exists for the position")

    elif code == 10040:
        print(f"Error: The limit of concurrent positions has been reached")

    elif code == 10041:
        print(f"Error: the pending order activation request for {symbol} has been rejected")

    elif code == 10042:
        print(f"Error: The request has been rejected because the 'Only long positions are allowed' rule is set for {symbol}")

    elif code == 10043:
        print(f"Error: The request has been rejected because the 'Only short positions are allowed' rule is set for {symbol}")

    elif code == 10044:
        print(f"Error: The request has been reject because the 'Only position closing is allowed' rule is set for {symbol}")

    elif code == 10045:
        print(f"Error: The request has been rejected because the 'Position closing is allowed only by FIFO rule' is set for the tradubg account")

    elif code == 10046:
        print(f"Error: The request has been rejected because the 'Opposite positions on a single symbol are diabled' rule is set for the trading account")


    #default
    else:
        print(f"Error lodging order for {symbol}. Error code: {code}. Order details: {code}")