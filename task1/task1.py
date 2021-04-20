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

#print("Weekly Returns:")
#print(aftWeeklyReturns)
#print("Monthly Returns:")
#print(aftMonthlyReturns)

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
#fig.savefig('MAVG.png')


#######################################
## Part 3
#######################################
start_date = '2020-02-01'
end_date = '2020-07-01'

# grab the crossover points from 10 day MAVG - 30 day MAVG
aftStockInfo["10d"] = aftStockInfo["Adj Close"].rolling(window = 10, center = False).mean()
aftStockInfo["30d"] = aftStockInfo["Adj Close"].rolling(window = 30, center = False).mean()
aftStockInfo["10d-30d"] = aftStockInfo["10d"] - aftStockInfo["30d"]

# for the specified dates
aftStockInfo["10d-30d"] = aftStockInfo["10d-30d"].loc[start_date:end_date]

# determine bullish or bearish using sign difference
aftStockInfo["Regime"] = np.where(aftStockInfo['10d-30d'] > 0, 1, 0)
aftStockInfo["Regime"] = np.where(aftStockInfo['10d-30d'] < 0, -1, aftStockInfo["Regime"])


# To ensure that all trades close out, temporarily change the regime of the last row to 0
regime_orig = aftStockInfo.loc[:, "Regime"].iloc[-1]
aftStockInfo.loc[:, "Regime"].iloc[-1] = 0
aftStockInfo["Signal"] = np.sign(aftStockInfo["Regime"] - aftStockInfo["Regime"].shift(1))
# Restore original regime data
aftStockInfo.loc[:, "Regime"].iloc[-1] = regime_orig

aftStockInfo.loc[aftStockInfo["Signal"] == 1, "Close"]
aftStockInfo.loc[aftStockInfo["Signal"] == -1, "Close"]
# Create a DataFrame with trades, including the price at the trade and the regime under which the trade is made.
aft_signals = pd.concat([
        pd.DataFrame({"Price": aftStockInfo.loc[aftStockInfo["Signal"] == 1, "Adj Close"],
                     "Regime": aftStockInfo.loc[aftStockInfo["Signal"] == 1, "Regime"],
                     "Signal": "Buy"}),
        pd.DataFrame({"Price": aftStockInfo.loc[aftStockInfo["Signal"] == -1, "Adj Close"],
                     "Regime": aftStockInfo.loc[aftStockInfo["Signal"] == -1, "Regime"],
                     "Signal": "Sell"}),
    ])
aft_signals.sort_index(inplace = True)
print(aft_signals)


# Let's see the profitability of long trades
aft_long_profits = pd.DataFrame({
        "Price": aft_signals.loc[(aft_signals["Signal"] == "Buy") &
                                  aft_signals["Regime"] == 1, "Price"],
        "Profit": pd.Series(aft_signals["Price"] - aft_signals["Price"].shift(1)).loc[
            aft_signals.loc[(aft_signals["Signal"].shift(1) == "Buy") & (aft_signals["Regime"].shift(1) == 1)].index
        ].tolist(),
        "End Date": aft_signals["Price"].loc[
            aft_signals.loc[(aft_signals["Signal"].shift(1) == "Buy") & (aft_signals["Regime"].shift(1) == 1)].index
        ].index
    })
print(aft_long_profits)



# locate data for only the specified dates
#strategyForGivenDates = aftStockInfo["Regime"].loc[start_date:end_date]

#print(strategyForGivenDates)#.value_counts())