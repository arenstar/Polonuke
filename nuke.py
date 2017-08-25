import time
import json
import requests
import hmac
import hashlib
import urllib

class Connection:
    def __init__(self, key="", secret="", timeout=30):
        self.key = key
        self.secret = secret
        self.timeout = timeout
        self.nonce = int(time.time()*1000000)

    def __call__(self, command, args={}):
        args['command'] = command
        args['nonce'] = self.nonce
        try:
            data = urllib.parse.urlencode(args)
            sign = hmac.new(self.secret.encode('utf-8'), data.encode('utf-8'), hashlib.sha512)
            response = requests.post('https://poloniex.com/tradingApi', data=args,
                                      headers={'Sign': sign.hexdigest(), 'Key': self.key},
                                      timeout=self.timeout)
        except Exception as exception: raise exception
        finally: self.nonce += 1
        try: return json.loads(response.text, parse_float=unicode)
        except NameError: return json.loads(response.text, parse_float=str)

def getTickers(market="BTC"):
    response = requests.get('https://poloniex.com/public?command=returnTicker').json()
    tickers = {}
    for ticker in response:
        if ticker.split('_')[0] == market:
            tickers[ticker] = response[ticker]['last']
    return tickers

def sellEverything(key="", secret="", market="BTC", limit=0.05, exceptions=[]):
    tickers = getTickers(market=market)
    A = Connection(key=key, secret=secret)
    balances = A('returnCompleteBalances')
    for ticker in balances:
        amount = float(balances[ticker]['available'])
        if float(amount) > 0:
            if ticker != market:
                if ticker not in exceptions:
                    response = A('sell', args={'currencyPair': "{0}_{1}".format(market, ticker), "rate": float(tickers["{0}_{1}".format(market, ticker)])*(1.0-limit), 'amount': amount})
                                 
