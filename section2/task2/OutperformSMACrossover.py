# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# first, REMEMBER to activate cryptoalgowheel-S2 environment!


# %%
from __future__ import (absolute_import, division, print_function, unicode_literals)

import os
import datetime
import sys

import backtrader as bt
import numpy as np
import pandas as pd
import matplotlib
import PyQt5


# %%
datadir = "../data"
logdir = "../log"
reportdir = "../report"
datafile = "BTC_USDT_1h.csv"
from_datetime = "2020-01-01 00:00:00"
to_datetime = "2020-04-01 00:00:00"



base/null.j2 [markdown]
# #### First experimental "Outperform Strategy"

# %%
logfile = "BTC_USDT_1h_OutperformSMACross1_2020-01-01_2020-04-01.csv"
figfile = "BTC_USDT_1h_OutperformSMACross1_2020-01-01_2020-04-01.png"


# %%
class OutperformSMACross_1(bt.Strategy):
    #***IMPORTANT: "parameters collection" that can be changed through passing-in later when "adding strategy";
    #usage of this "parameters collection" later: use "self.params.xxx"!
    params = (
    #***"pfast" and "pslow" are parameters for "bt.ind.SMA" instance (the SMA indicator object in the package)!!
        ("pfast", 10),       # "pfast": 'fast' moving average (default period 10)
        ("pslow", 20),       # "pslow": 'slow' moving average (default period 20)
    )

    def __init__(self):
        self.dataclose = self.datas[0].close

        # add Moving Average related indicators
        self.fastsma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.pfast)
        self.slowsma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.pslow)

    def next(self):
        # suppose: still Double SMA Crossover strategy logic
        if not self.position:
            if (self.fastsma[-1] <= self.slowsma[-1]) and (self.fastsma[0] > self.slowsma[0]):
                self.buy()
        else:
            if (self.fastsma[-1] >= self.slowsma[-1]) and (self.fastsma[0] < self.slowsma[0]):
                self.sell()


# %%
cerebro = bt.Cerebro()

#feed data:
data = pd.read_csv(os.path.join(datadir, datafile), index_col="datetime", parse_dates=True)
data = data.loc[(data.index >= pd.to_datetime(from_datetime)) & (data.index <= pd.to_datetime(to_datetime))]    #(datafile already corresponding to the required time-frame: just in case here)
datafeed = bt.feeds.PandasData(dataname=data, timeframe=bt.TimeFrame.Minutes, compression=60)      #[*! Detail: specify as "Hourly Data"]
cerebro.adddata(datafeed)

#add strategy:
cerebro.addstrategy(OutperformSMACross_1, pfast=10, pslow=50)     #***Notice: passing in different parameter values (used in the strategy class) here!!!
#*** Here, try changing the period of the "slow" SMA to 50 (from default 20)!

cerebro.addsizer(bt.sizers.PercentSizer, percents=99) #this PercentSizer sizer object returns percents of available cash
#* here, parameter "percents=99" means using 99% of all currently available cash (to trade) (not completely "All-In"(100%))

cerebro.broker.set_cash(10000)
cerebro.broker.setcommission(commission=0.001)

#add logger
cerebro.addwriter(bt.WriterFile, out=os.path.join(logdir, logfile), csv=True)       #there is only a single Writer defined called WriterFile, which can be added to the system
#by calling cerebro.addwriter(writerclass, **kwargs), writerclass will be instantiated during backtesting execution with the given kwargs
#[documentation: https://www.backtrader.com/docu/writer/]

#run
cerebro.run()

#save graph report
#(*! use PyQt5 backend on matplotlib here (Mac)!!)
matplotlib.use("Qt5Agg")
fig = cerebro.plot(height=30, width=60, style="candlestick", barup="green", bardown="red", iplot=False)
fig[0][0].savefig(os.path.join(reportdir, figfile), dpi=480)
#cerebro.plot(height=30, width=60, style="candlestick", barup="green", bardown="red", iplot=False)

base/null.j2 [markdown]
# By changing the period of one of the two moving averages (the "slow SMA" here), we can see that the final value of our strategy changed accordingly. Here, with a "slower" moving average (the original 'slow SMA' calculated based on a wider time-frame: 50-bar period instead of the original 20-bar period), we got a \$10655.74 final value, which was \$654.43 higher than the final value of the original "10(fast)-20(slow)" Double SMA Crossover strategy ($10001.31). This could be because the original 20-bar period might be a little too "fast-changing" still for the Slow SMA line, making the strategy less robust and causing still excessive Buy & Sell trades executed (too frequent changes of position) rather than necessary. The somehow longer 50-bar period for the Slow SMA line might be more appropriate here.



base/null.j2 [markdown]
# #### Second experimental "Outperform Strategy"

# %%
logfile = "BTC_USDT_1h_OutperformSMACross2_2020-01-01_2020-04-01.csv"
figfile = "BTC_USDT_1h_OutperformSMACross2_2020-01-01_2020-04-01.png"


# %%
class OutperformSMACross_2(bt.Strategy):
    #***IMPORTANT: "parameters collection" that can be changed through passing-in later when "adding strategy";
    #usage of this "parameters collection" later: use "self.params.xxx"!
    params = (
    #***"pfast" and "pslow" are parameters for "bt.ind.SMA" instance (the SMA indicator object in the package)!!
        ("pfast", 10),       # "pfast": 'fast' moving average (default period 10)
        ("pslow", 20),       # "pslow": 'slow' moving average (default period 20)
    )

    def __init__(self):
        self.dataclose = self.datas[0].close

        # *** add Exponential Moving Average indicators here
        self.fastsma = bt.indicators.ExponentialMovingAverage(self.datas[0], period=self.params.pfast)
        self.slowsma = bt.indicators.ExponentialMovingAverage(self.datas[0], period=self.params.pslow)

    def next(self):
        # suppose: still Double SMA Crossover strategy logic
        if not self.position:
            if (self.fastsma[-1] <= self.slowsma[-1]) and (self.fastsma[0] > self.slowsma[0]):
                self.buy()
        else:
            if (self.fastsma[-1] >= self.slowsma[-1]) and (self.fastsma[0] < self.slowsma[0]):
                self.sell()


# %%
cerebro = bt.Cerebro()

#feed data:
data = pd.read_csv(os.path.join(datadir, datafile), index_col="datetime", parse_dates=True)
data = data.loc[(data.index >= pd.to_datetime(from_datetime)) & (data.index <= pd.to_datetime(to_datetime))]    #(datafile already corresponding to the required time-frame: just in case here)
datafeed = bt.feeds.PandasData(dataname=data, timeframe=bt.TimeFrame.Minutes, compression=60)      #[*! Detail: specify as "Hourly Data"]
cerebro.adddata(datafeed)

#add strategy:
cerebro.addstrategy(OutperformSMACross_2, pfast=10, pslow=50)     #***Notice: passing in different parameter values (used in the strategy class) here!!!
#*** Here, try changing the period of the "slow" SMA to 50 (from default 20)!

cerebro.addsizer(bt.sizers.PercentSizer, percents=99) #this PercentSizer sizer object returns percents of available cash
#* here, parameter "percents=99" means using 99% of all currently available cash (to trade) (not completely "All-In"(100%))

cerebro.broker.set_cash(10000)
cerebro.broker.setcommission(commission=0.001)

#add logger
cerebro.addwriter(bt.WriterFile, out=os.path.join(logdir, logfile), csv=True)       #there is only a single Writer defined called WriterFile, which can be added to the system
#by calling cerebro.addwriter(writerclass, **kwargs), writerclass will be instantiated during backtesting execution with the given kwargs
#[documentation: https://www.backtrader.com/docu/writer/]

#run
cerebro.run()

#save graph report
#(*! use PyQt5 backend on matplotlib here (Mac)!!)
matplotlib.use("Qt5Agg")
fig = cerebro.plot(height=30, width=60, style="candlestick", barup="green", bardown="red", iplot=False)
fig[0][0].savefig(os.path.join(reportdir, figfile), dpi=480)
#cerebro.plot(height=30, width=60, style="candlestick", barup="green", bardown="red", iplot=False)

base/null.j2 [markdown]
# In this strategy using two Exponential Moving Average lines with fast period of 10 and slow period of 50 (following the prior first experiment), we obtained a final value of \$12942.65, \$2941.34 dollar more than that of the original Double SMA Crossover strategy ($10001.31). This result was even better than the first experiment above. As the exponential moving averages give greater weight to the more recent price moves, they are able to react to the dynamics of closer trends more swiftly than the historically further-away trends, compared to the Simple Moving Averages which give equal weights to price moves in different distances of times. Applying Exponential moving averages might be even more appropriate here. Interestingly, also notice from the report graph of this strategy that under this usage of exponential moving averages instead of simple moving averages here, the frequency of (buy & sell) transactions seemed even lower than that in the previous scenarios, indicating that indeed, through avoiding too frequent trades sometimes could improve our performance.<br>
# There's one potential conclusion we may draw from our experiments here that shorter-term moving averages tend to be less effective than longer-term moving averages, which increase the robustness of the strategy and prevent obsessively frequent trades that might lead to further loss.<br>
# (some reference: https://decodingmarkets.com/moving-average-crossover-strategies/)



base/null.j2 [markdown]
# #### Third experimental "Outperform Strategy"

# %%
logfile = "BTC_USDT_1h_OutperformSMACross3_2020-01-01_2020-04-01.csv"
figfile = "BTC_USDT_1h_OutperformSMACross3_2020-01-01_2020-04-01.png"


# %%
class OutperformSMACross_3(bt.Strategy):
    #***IMPORTANT: "parameters collection" that can be changed through passing-in later when "adding strategy";
    #usage of this "parameters collection" later: use "self.params.xxx"!
    params = (
    #***"pfast" and "pslow" are parameters for "bt.ind.SMA" instance (the SMA indicator object in the package)!!
        ("pfast", 10),       # "pfast": 'fast' moving average (default period 10)
        ("pslow", 20),       # "pslow": 'slow' moving average (default period 20)
    )

    def __init__(self):
        self.dataclose = self.datas[0].close

        # *** add Exponential Moving Average indicators here
        self.fastsma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.pfast)
        self.slowsma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.pslow)

    def next(self):
        # *** New added logic to DoubleSMACrossover strategy here: recognize "REAL" Golden Cross / Death Cross and "FAKE" Golden Cross / Death Cross
        # ** "REAL" Golden Cross: fast SMA line crosses slow SMA line from below AND *slow SMA keeps the rising trend;
        # ** "FAKE" Golden Cross: fast SMA line crosses slow SMA line from below BUT slow SMA actually is under the downward trend;
        # ** "REAL" Death Cross: fast SMA line crosses slow SMA line from above AND *slow SMA keeps the declining trend;
        # ** "FAKE" Death Cross: fast SMA line crosses slow SMA line from above BUT slow SMA actually is under a rising trend
        if not self.position:
            if (self.fastsma[-1] <= self.slowsma[-1]) and (self.fastsma[0] > self.slowsma[0]) and (self.slowsma[-1] < self.slowsma[0]):  #added condition: Slow SMA line under a rising trend
                self.buy()
        else:
            if (self.fastsma[-1] >= self.slowsma[-1]) and (self.fastsma[0] < self.slowsma[0]) and (self.slowsma[-1] > self.slowsma[0]): #added condition: Slow SMA line under a declining trend
                self.sell()

base/null.j2 [markdown]
# ##### "REAL" & "FAKE" Golden Cross / Death Cross strategy reference: http://www.360doc.com/content/11/1017/19/3329613_156955198.shtml

# %%
cerebro = bt.Cerebro()

#feed data:
data = pd.read_csv(os.path.join(datadir, datafile), index_col="datetime", parse_dates=True)
data = data.loc[(data.index >= pd.to_datetime(from_datetime)) & (data.index <= pd.to_datetime(to_datetime))]    #(datafile already corresponding to the required time-frame: just in case here)
datafeed = bt.feeds.PandasData(dataname=data, timeframe=bt.TimeFrame.Minutes, compression=60)      #[*! Detail: specify as "Hourly Data"]
cerebro.adddata(datafeed)

#add strategy:
cerebro.addstrategy(OutperformSMACross_3, pfast=10, pslow=50)     #***Notice: passing in different parameter values (used in the strategy class) here!!!
#*** Here, try changing the period of the "slow" SMA to 50 (from default 20)!

cerebro.addsizer(bt.sizers.PercentSizer, percents=99) #this PercentSizer sizer object returns percents of available cash
#* here, parameter "percents=99" means using 99% of all currently available cash (to trade) (not completely "All-In"(100%))

cerebro.broker.set_cash(10000)
cerebro.broker.setcommission(commission=0.001)

#add logger
cerebro.addwriter(bt.WriterFile, out=os.path.join(logdir, logfile), csv=True)       #there is only a single Writer defined called WriterFile, which can be added to the system
#by calling cerebro.addwriter(writerclass, **kwargs), writerclass will be instantiated during backtesting execution with the given kwargs
#[documentation: https://www.backtrader.com/docu/writer/]

#run
cerebro.run()

#save graph report
#(*! use PyQt5 backend on matplotlib here (Mac)!!)
matplotlib.use("Qt5Agg")
fig = cerebro.plot(height=30, width=60, style="candlestick", barup="green", bardown="red", iplot=False)
fig[0][0].savefig(os.path.join(reportdir, figfile), dpi=480)
#cerebro.plot(height=30, width=60, style="candlestick", barup="green", bardown="red", iplot=False)

base/null.j2 [markdown]
# This updated double SMA crossover strategy (fast SMA period - 10, slow SMA period - 50, as following the previous two experiments) with additional checking mechanism of "real" or "fake" Golden Cross (Buy signal) and Death Cross (Exit signal) improves our final trading results compared to the original DoubleSMACrossover again. Though earning a little bit less than the previous second strategy using exponential moving averages, it still gives us a quite decent final value of \$12007.22 (~20% return from the \$10000 original money available in the beginning), earning \$2005.91 more than the original DoubleSMACrossover strategy. Many may take any "crossover" of the two moving average lines as signals; however, this is not the case all the time. Besides the normal "crossover" occurrences we normally regard as signals, we often need to take into consideration whether the longer term trend is truly rising or declining as well. Say, if a golden cross appears (fast SMA crosses slow SMA from below to above) but actually the longer term still is indicating a bearish (downward) trend as shown by the slow SMA, the market dynamic is actually not prospering enough to provide sufficient evidence for justifying a BUY order decision; thus, this situation is actually considered a "false signal" of golden cross. (similar for the "fake" death cross scenario as reversal signal.) This updated strategy now enables us to sidestep those "fake signals" and avoid making mistakes trading at false timings.<br>
# <br>
# (some thoughts on additional improvement/optimization could be to implement this updated strategy with "fake signal" checking mechanism on exponential moving averages indicators or others.)

# %%



