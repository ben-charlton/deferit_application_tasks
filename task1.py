import pandas as pd

aftStockInfo = pd.read_csv (r'APT.AX.csv')
aftStockInfo['Date'] = pd.to_datetime(aftStockInfo['Date'])
print (aftStockInfo)

aftWeeklyReturns = aftStockInfo['Adj Close'].resample('M', on='date').ffill().pct_change()

print("weekly price = " + aftWeeklyReturns)