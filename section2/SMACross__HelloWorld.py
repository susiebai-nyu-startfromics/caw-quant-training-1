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
logfile = "BTC_USDT_1h_SMACross_10_20_2020-01-01_2020-04-01.csv"
figfile = "BTC_USDT_1h_SMACross_10_20_2020-01-01_2020-04-01.png"
from_datetime = "2020-01-01 00:00:00"
to_datetime = "2020-04-01 00:00:00"


# %%
class SMACross(bt.Strategy):
    #***IMPORTANT: "parameters collection" that can be changed through passing-in later when "adding strategy";
    #usage of this "parameters collection" later: use "self.params.xxx"!
    params = (
    #***"pfast" and "pslow" are parameters for "bt.ind.SMA" instance (the SMA indicator object in the package)!!
        ("pfast", 10),       # "pfast": 'fast' moving average
        ("pslow", 20),       # "pslow": 'slow' moving average
    )

    def __init__(self):
        self.dataclose = self.datas[0].close

        #add SimpleMovingAverage indicator(s)
        self.fastsma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.pfast)
        self.slowsma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.pslow)

    def next(self):      #similar to naive HelloWorld strategy written last time

        if not self.position:      #not yet in market
            if self.dataclose[0] > self.slowsma[0]:    #logic: if current close price becomes higher ("cross from below") than the 'slow SMA' - buy
                self.buy()
        else:      #already in market
            if self.dataclose[0] < self.slowsma[0]:    #logic: then if current close price becomes lower ("cross from above") than the 'slow SMA' - sell
                self.sell()


# %%
cerebro = bt.Cerebro()

#feed data:
data = pd.read_csv(os.path.join(datadir, datafile), index_col="datetime", parse_dates=True)     #***IMPORTANT DETAIL: Must set "datetime" columm as the "index" of the pandas DataFrame!!!
data = data.loc[(data.index >= pd.to_datetime(from_datetime)) & (data.index <= pd.to_datetime(to_datetime))]    #(datafile already corresponding to the required time-frame: just in case here)
datafeed = bt.feeds.PandasData(dataname=data, timeframe=bt.TimeFrame.Minutes, compression=60)         #[*!!]Notice detail: dataset representing "Hourly" data here (https://community.backtrader.com/topic/453/hourly-data)
cerebro.adddata(datafeed)

#add strategy:
cerebro.addstrategy(SMACross)

cerebro.addsizer(bt.sizers.PercentSizer, percents=99) #this PercentSizer sizer object returns percents of available cash
#* here, parameter "percents=99" means using 99% of all currently available cash (to trade) (not completely "All-In"(100%))

cerebro.broker.set_cash(10000)
cerebro.broker.setcommission(commission=0.001)

#[***] prepare file names of "log file" and "report (graph) file"
#{pending}

#add logger
cerebro.addwriter(bt.WriterFile, out=os.path.join(logdir, logfile), csv=True)       #there is only a single Writer defined called WriterFile, which can be added to the system
#by calling cerebro.addwriter(writerclass, **kwargs), writerclass will be instantiated during backtesting execution with the given kwargs
#[documentation: https://www.backtrader.com/docu/writer/]


#run
cerebro.run()


#save graph report
#(*! use PyQt5 backend on matplotlib here (Mac)!!)
matplotlib.use("Qt5Agg")
fig = cerebro.plot(height=30, style="candlestick", barup="green", bardown="red", iplot=False)
fig[0][0].savefig(os.path.join(reportdir, figfile), dpi=480)
#cerebro.plot(height=30, width=60, style="candlestick", barup="green", bardown="red", iplot=False)


# %%
print(cerebro.strats[0][0][0])
#Note: this shows the specific strategy class created here ("SMACross" class object here)


# %%
cerebro.strats[0][0][0].params.__dict__
#Note: this shows all the parameter values specified for the strategy class
#(shown at the end of the parameter dictionary)


# %%
tuple(cerebro.strats[0][0][0].params.__dict__.items())[5:]     #all 'useful' parameter values specified for the strategy class


# %%
#display corresponding parameter & value:
print("pfast:", cerebro.strats[0][0][0].params.__dict__["pfast"])
print("pslow:", cerebro.strats[0][0][0].params.__dict__["pslow"])


# %%
#SMACross.params.__dict__


# %%



