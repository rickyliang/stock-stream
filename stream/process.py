import requests
import threading
from time import sleep
from config import UPDATE_INTERVAL
from util import get_session
from models import Stock



# Url that is used in process.py to retrieve live data
STREAM_URL = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20' \
    'yahoo.finance.quotes%20where%20symbol%20in%20({0})&format=json&env=store%' \
    '3A%2F%2Fdatatables.org%2Falltableswithkeys&callback='

class Streamer:
    
    def __init__(self):
        self.running = True
        self.threads = []
        self.stocks = []
        self.stocks_csv = ""
        
        # Load from the database the previously-stored quotes.
        self.load()
        
    def is_valid_symbol(self, symbol):
        """
        Checks if the symbol is a string.
        
        @return True if it is of primitive type str, False otherwise.
        """
        return type(symbol) is str
    
    def update(self):
        while self.running:
            if len(self.stocks) > 0:
                # Retrieve a response object from Yahoo's YQL service.
                try:
                    stocks_json_request = requests.get(STREAM_URL.format(repr(self.stocks_csv)))
                except requests.ConnectionError as e:
                    print('Cannot connect to the service. Please check your connection.')
                    print('Trying again in {} seconds.'.format(UPDATE_INTERVAL))
                except requests.HTTPError as e:
                    print(e)
                except:
                    print('Could not retrieve the json from the specified URL.')
                
                # Retrieve the json data from the response.
                try:
                    stocks_json_data = stocks_json_request.json()
                except ValueError as e:
                    print(e)
                    print('Something bad occurred when trying to update the stocks '
                        'from Yahoo\'s YQL service.')
                        
                # Retrieve a list of each stock's data, which are stored as dictionaries.
                stocks_data_list = stocks_json_data['query']['results']['quote']
                if type(stocks_data_list) is dict:  # Occurs when only one stock entry.
                    stocks_data_list = [stocks_data_list]
                
                # Update each stock's data.
                with get_session() as session:
                    for stock_data in stocks_data_list:
                        stock = session.query(Stock).filter(Stock.symbol == stock_data['Symbol']).first()
                        stock.last_trade_price = stock_data['LastTradePriceOnly']
                        session.add(stock)
                        print('\nSymbol: ' + stock.symbol)
                        print('Price: ' + stock.last_trade_price)
                        
                    # Commit the changes.
                    session.commit()
                    
                    print('- - - - - - - - - - - - - - -')
                    
                    # Warn the user if number of stocks in the database mismatch with
                    # the number of stocks the application is attempting to update.
                    num_stocks = session.query(Stock).count()
                    if num_stocks != len(self.stocks):
                        print('Warning: the number of stocks in the database do not match '
                            'the number of stocks this program is updating.')
                        print('Some data may not be refreshing and will be inaccurate.')
                
            sleep(UPDATE_INTERVAL)
            
    def get_user_input(self):
        """
        DEBUGGING PURPOSES ONLY.
        To run with this option, start the app with the --debug parameter.
        """
        print("Enter 'quitnow' to exit, 'help' for information.")
        while True:
            input = raw_input('> ')
            input = input.upper()
            parsed = input.split()
            try:
                if parsed[0] == 'QUITNOW':
                    self.running = False
                    break
                elif parsed[0] == 'HELP':
                    print("\nA list of commands.")
                    print("'add SYMBOL' -- add a stock symbol to the database.")
                    print("'remove SYMBOL' -- remove a stock symbol from the database")
                    print("'quitnow' -- exit the application.\n")
                elif parsed[0] == 'ADD':
                    self.add(parsed[1])
                elif parsed[0] == 'REMOVE':
                    self.remove(parsed[1])
                else:
                    print('')
            except IndexError:
                pass
        
    def add(self, symbol):
        """
        Adds a symbol to the Streamer. add updates the Streamer's stocks
        array, stocks_csv string, and puts the symbol into the database.
        
        @symbol a string of a stock's ticker symbol.
        """
        if self.is_valid_symbol(symbol):
            symbol = symbol.upper()
            in_local = self.find_local(symbol) is not None
            in_database = self.find_database(symbol) is not None
            if not in_local:
                self.stocks.append(symbol)
                self.stocks_csv = '","'.join(self.stocks)
            if not in_database:
                new_stock = Stock(symbol)
                with get_session() as session:
                    session.add(new_stock)
                    session.commit()
        else:
            print('Symbol must be a string.')
            
    def find_local(self, symbol):
        """
        Searches this Streamer instance's stocks array for the symbol.
        Useful for populating the Streamer stocks array when re-initiating
        the program.
        
        @symbol a string of a stock's ticker symbol.
        @return the symbol if it exists, None otherwise.
        """
        if symbol in self.stocks:
            return symbol
        else:
            return None
            
    def find_database(self, symbol):
        """
        Searches the database for the symbol.
        
        @symbol a string of a stock's ticker symbol.
        @return the object if it exists, None otherwise.
        """
        with get_session() as session:
            stock = session.query(Stock).filter(Stock.symbol == symbol).first()
        return stock
        
    def load(self):
        """
        Searches the database and populates the Streamer instance with the
        quotes that it needs to retrieve from YQL.
        """
        with get_session() as session:
            stocks_in_database = session.query(Stock).all()
        for stock in stocks_in_database:
            self.add( str(stock.symbol) )
            
    def remove(self, symbol):
        """
        Removes a symbol to the Streamer. remove updates the Streamer's stocks
        array, stocks_csv string, and deletes the symbol from the database.
        
        @symbol a string of a stock's ticker symbol.
        """
        if self.is_valid_symbol(symbol):
            symbol = symbol.upper()
            in_local = self.find_local(symbol) is not None
            in_database = self.find_database(symbol) is not None
            if in_local and in_database:
                self.stocks.remove(symbol)
                self.stocks_csv = '","'.join(self.stocks)
                with get_session() as session:
                    stock = session.query(Stock).filter(Stock.symbol == symbol).first()
                    session.delete(stock)
                    session.commit()
            elif not in_local:
                print('Symbol {} is not in the local stocks array.'.format(symbol))
            else:
                print('Symbol {} is not in the database.'.format(symbol))
        else:
            print('Symbol must be a string.') 
            
    def run(self, debug=False):
        thread1 = threading.Thread(target=self.update)
        # Make threads daemonic, i.e. terminate them when main thread terminates.
        # http://stackoverflow.com/questions/12376224/python-threadin
        # g-running-2-different-functions-simultaneously
        thread1.daemon = True
        thread1.start()
        self.threads.append(thread1)
        if debug:
            thread2 = threading.Thread(target=self.get_user_input)
            thread2.daemon = True
            thread2.start()
            self.threads.append(thread2)