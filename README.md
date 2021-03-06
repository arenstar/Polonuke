<p align="center"><img src="https://github.com/Crypto-AI/Polonuke/blob/master/bomb.png" width="100px"></p>

<i>
The script below will attempt to sell everything with a balance on your account on the BTC market. It will leave ETH and GAME untouched as they are listed as exceptions. To sell the rest of the coins, for each one, it will cancel any open orders and then sell at 5% below the last price to simulate a market sell. This essentially tells Poloniex, sell immediately at the next best price but if the volatility causes the price to wick down more than 5%, cancel any open orders but don't sell.
</i>
<br><br>

```text
git clone https://github.com/Crypto-AI/Polonuke
cd Polonuke
```

```python
import nukem

nukem.sellEverything(key="", secret="", market="BTC", limit=0.05, exceptions=['ETH', 'GAME']):
```

<br><br>
<i>
Note: This script cannot cancel stop loss orders which will restrict the available balance to sell due to Poloniex API limitations.
</i>
