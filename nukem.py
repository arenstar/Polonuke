import time
import json
import requests
import hmac
import hashlib
import urllib

class Connection:
    def __init__(self, key="", secret="", timeout=30):
        self.key     = key
        self.secret  = secret
        self.nonce   = 1503688733019678+int(time.time())-1503677725
        self.timeout = timeout

    def __call__(self, command, args={}):
        args['command'] = command
        args['nonce'] = self.nonce
        try:
            data = urllib.parse.urlencode(args)
            sign = hmac.new(self.secret.encode('utf-8'), data.encode('utf-8'), hashlib.sha512)
            response = requests.post('https://poloniex.com/tradingApi', data=args,
                                      headers={'Sign': sign.hexdigest(), 'Key': self.key},
                                      timeout=self.timeout)
        except Exception as exception: 
            raise exception
        finally:
            self.nonce += 1
        try: 
            return json.loads(response.text, parse_float=unicode)
        except NameError: 
            return json.loads(response.text, parse_float=str)

def getTickers(market="BTC"):
    response = requests.get('https://poloniex.com/public?command=returnTicker').json()
    tickers = {}
    for ticker in response:
        if ticker.split('_')[0] == market:
            tickers[ticker] = response[ticker]['last']
    return tickers

def sellEverything(key="", secret="", market="BTC", limit=0.05, exceptions=[]):
    exceptions = [x.upper() for x in exceptions]
    
    # Get all active tickers on a market with last price
    tickers = getTickers(market=market)
    
    # Get a list of balances and orders
    A = Connection(key=key, secret=secret)
    balances = A('returnCompleteBalances')

    try:
        print(balances['error'])
        return
    except KeyError:
        pass

    # Start canceling orders and selling coins
    for ticker in balances:
        available = float(balances[ticker]['available'])
        totalAmount = available+float(balances[ticker]['onOrders'])
        if totalAmount > 0:
            if ticker != market:
                if ticker not in exceptions:
                    
                    # Cancel any open orders (cannot cancel stop limits)
                    orders = A('returnOpenOrders', args={'currencyPair': "{0}_{1}".format(market, ticker)})
                    try:
                        print(orders['error'])
                    except TypeError:
                        pass
                    except KeyError:
                        pass

                    if len(orders) > 0:
                        print("Cancelling orders for {0}_{1}...".format(market, ticker))
                        for order in orders:
                            response = A('cancelOrder', args={'orderNumber': order['orderNumber']})
                            if response['error']:
                                print(response['error'])
                                
                    # Give those Poloniex basement servers a second to cancel the orders
                    time.sleep(1)
                            
                    # Sell slightly below (default=5%) the last price  
                    print("Market selling {0}_{1}...".format(market, ticker))     
                    response = A('sell', args={'currencyPair': "{0}_{1}".format(market, ticker), "rate": float(tickers["{0}_{1}".format(market, ticker)])*(1.0-limit), 'amount': totalAmount})   
                    try:
                        if response['error'] == "Not enough {0}.".format(ticker):
                            if available > 0:
                                response = A('sell', args={'currencyPair': "{0}_{1}".format(market, ticker), "rate": float(tickers["{0}_{1}".format(market, ticker)])*(1.0-limit), 'amount': available})   
                                try:
                                    print(response['error'])
                                except KeyError:
                                    pass                                    
                            else:
                                print("You probably have a stop-limit set that cannot be canceled.")
                        else:
                            print(response['error'])
                    except KeyError:
                        pass
