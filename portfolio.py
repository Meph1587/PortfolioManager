

import datetime
from time import sleep
from binance.client import Client

client = Client("", "")

COIN1= client.get_historical_klines(symbol='ETHBTC', interval= '4h', start_str= '2018.07.01', end_str= '2018.07.25')
COIN2= client.get_historical_klines(symbol='IOTABTC', interval= '4h', start_str= '2018.07.01', end_str= '2018.07.25')
COIN3= client.get_historical_klines(symbol='ADABTC', interval= '4h', start_str= '2018.07.01', end_str= '2018.07.25')
COIN4= client.get_historical_klines(symbol='BNBBTC', interval= '4h', start_str= '2018.07.01', end_str= '2018.07.25')
COIN5= client.get_historical_klines(symbol='NEOBTC', interval= '4h', start_str= '2018.07.01', end_str= '2018.07.25')

import numpy as np
import pandas as pd

COIN1_df= pd.DataFrame(COIN1, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
COIN2_df= pd.DataFrame(COIN2, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
COIN3_df= pd.DataFrame(COIN3, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
COIN4_df= pd.DataFrame(COIN4, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
COIN5_df= pd.DataFrame(COIN5, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])

COIN1_df['Open time']= pd.to_datetime(COIN1_df['Open time'], unit='ms')
COIN2_df['Open time']= pd.to_datetime(COIN2_df['Open time'], unit='ms')
COIN3_df['Open time']= pd.to_datetime(COIN3_df['Open time'], unit='ms')
COIN4_df['Open time']= pd.to_datetime(COIN4_df['Open time'], unit='ms')
COIN5_df['Open time']= pd.to_datetime(COIN5_df['Open time'], unit='ms')

COIN1_df.set_index('Open time', inplace=True)
COIN2_df.set_index('Open time', inplace=True)
COIN3_df.set_index('Open time', inplace=True)
COIN4_df.set_index('Open time', inplace=True)
COIN5_df.set_index('Open time', inplace=True)
COIN1_df['Close']= COIN1_df['Close'].astype(float)
COIN2_df['Close']= COIN2_df['Close'].astype(float)
COIN3_df['Close']= COIN3_df['Close'].astype(float)
COIN4_df['Close']= COIN4_df['Close'].astype(float)
COIN5_df['Close']= COIN5_df['Close'].astype(float)

coins= pd.concat([COIN1_df['Close'], COIN2_df['Close'], COIN3_df['Close'], COIN4_df['Close'], COIN5_df['Close']], axis=1)
coins.columns= ['COIN1', 'COIN2', 'COIN3', 'COIN4', 'COIN5']
coins.corr()

daily_return= coins.pct_change().dropna()
q1_return= daily_return.mean()*90
q1_cov= daily_return.cov()*90

pf_returns, pf_volatility, pf_sharpe_ratio, pf_coins_weights=([] for i in range(4))
num_portfolios= 10000
for portfolio in range(num_portfolios):
    weights= np.random.random(5)
    weights /= np.sum(weights)
    returns = np.dot(weights, q1_return)
    volatility = np.sqrt(np.dot(weights.T, np.dot(q1_cov, weights)))
    sharpe = returns / volatility
    pf_coins_weights.append(weights)
    pf_returns.append(returns)
    pf_volatility.append(volatility)
    pf_sharpe_ratio.append(sharpe)

import matplotlib.pyplot as plt
#import seaborn as sns

plt.figure(figsize=(15,7))
plt.scatter(x=pf_volatility, y=pf_returns, c= pf_sharpe_ratio, cmap='viridis')
plt.colorbar(label='Sharpe Ratio')
#sns.set(style='darkgrid')
plt.title('Efficient Frontier')
plt.xlabel('Volatility')
plt.ylabel('Return')
plt.show()


print ( "bets value" + str(max(pf_sharpe_ratio)))

print ("   ETH    ,   IOTA    ,     ADA    ,   BNB     ,  NEO    ")
print (str(pf_coins_weights[pf_sharpe_ratio.index(max(pf_sharpe_ratio))]) + " best risk/return " )

print (str(pf_coins_weights[pf_volatility.index(min(pf_volatility))]) + " best minimum risk"  )

#print (str(pf_coins_weights[pf_returns.index(max(pf_returns))]) + " best maximize returns ")

coins_normed= coins/coins.iloc[0]
coins_normed.plot(figsize=(15,7))

