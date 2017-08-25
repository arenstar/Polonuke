# Polonuke
Nuke your alts before BTC destroys your portfolio

```text
git clone https://github.com/Crypto-AI/Polonuke
cd Polonuke
pip install -r requirements.txt
```

```python
import nukem

nukem.sellEverything(key="", secret="", market="BTC", limit=0.05, exceptions=['ETH', 'GAME']):
```

<i>The above script will attempt to sell everything with a balance on your account on the BTC market. It will leave ETH and GAME (legends never sell) untouched as they are listed as exceptions. To sell the rest of the coins, for each one, it will cancel any open orders and then sell at 5% below the last price to simulate a market sell. This essentially tells Poloniex, sell immediately at the next best price but if the volatility causes the price to wick down 5%, cancel the order but don't sell.</i>
