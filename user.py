



class User(object):

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, name: str):
        self.__name = name

    @property
    def login(self) -> int:

        return self.__login
    
    @login.setter
    def login(self, login: int):

        self.__login = login

    @property
    def password(self) -> str:

        return self.__password
    
    @password.setter
    def password(self, password: str):

        self.__password = password

    @property
    def server(self) -> str:

        return self.__server
    
    @server.setter
    def server(self, server: str):

        self.__server = server

    @property
    def path(self) -> str:
        return self.__path
    
    @path.setter
    def path(self, path: str):
        self.__path = path

    


    #Constructor
    def __init__(self, name: str, login: int, password: str, server: str, deriv = False):

        self.name = name
        self.login = login
        self.password = password
        self.server = server

        if deriv:
            path = "C:\\Program Files\\MetaTrader\\terminal64.exe"

        else:
            path = "C:\\Program Files\\MetaTrader 5\\terminal64.exe"

        self.path = path

        
    #Function to retrieve default user
    def get_user(broker: str) -> dict: 
        """
        Function to retrieve login information for the default trading account.
        This account will be used to access symbol information and candles.
        :return json: Returns Json in the form of a dictionary with login info
        """

        global mt5
        global deriv_drv
        global deriv_fx
        global xm
        global octa

        if broker.lower() == "mt5":
            return mt5

        if broker.lower() == "deriv-drv":
            return deriv_drv

        if broker.lower() == "deriv-fx":
            return deriv_fx

        if broker.lower() == "xm":
            return xm

        if broker.lower() == "octa":
            return octa

        raise Exception("Unknown broker. Please enter one of the brokers provided in the list")



    