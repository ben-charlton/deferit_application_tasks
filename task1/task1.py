import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# grab the data into an object from the csv
aftStockInfo = pd.read_csv (r'APT.AX.csv')
# convert the date column to a datetime so we can manipulate the data based on dates
aftStockInfo['Date'] = pd.to_datetime(aftStockInfo['Date'])
aftStockInfo = aftStockInfo.set_index('Date')


#######################################
## Part 1
#######################################
# calculate weekly and monthly average price (of the adj closing price)
aftWeeklyReturns = aftStockInfo['Adj Close'].resample('W').mean().ffill()
aftMonthlyReturns = aftStockInfo['Adj Close'].resample('M').mean().ffill()

print("Weekly Returns:")
print(aftWeeklyReturns)
print("Monthly Returns:")
print(aftMonthlyReturns)

#######################################
## Part 2
#######################################
# calculate 30 day MAVG and 10 day MAVG
tenDayMavg = aftStockInfo.rolling(window=10).mean()
thirtyDayMavg = aftStockInfo.rolling(window=30).mean()

# create the plot and then overlay the trendlines
start_date = '2020-04-16'
end_date = '2021-04-16'
fig, ax = plt.subplots(figsize=(16,9))
ax.plot(thirtyDayMavg.loc[start_date:end_date, :].index, thirtyDayMavg.loc[start_date:end_date, 'Adj Close'], label = '30 day MAVG')
ax.plot(tenDayMavg.loc[start_date:end_date, :].index, tenDayMavg.loc[start_date:end_date, 'Adj Close'], label = '10 day MAVG')
ax.legend(loc='best')
ax.set_ylabel('Adj Close')

# save the graph as a png file for easy viewing 
fig.savefig('MAVG.png')


#######################################
## Part 3
#######################################
start_date = '2020-02-01'
end_date = '2020-07-01'

trading_position = (tenDayMavg - thirtyDayMavg).apply(np.sign)
print(trading_position.tail())

#https://www.learndatasci.com/tutorials/python-finance-part-3-moving-average-trading-strategy/
#https://www.investopedia.com/articles/active-trading/052014/how-use-moving-average-buy-stocks.asp
