# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# first, REMEMBER to activate cryptoalgowheel-S2 environment!


# %%
import datetime
import os
import sys

import backtrader as bt
import numpy as np
import pandas as pd
import matplotlib
import PyQt5


# %%
#*****WARNING: REVISE THE "dir" FOLDER PATHS!!!
datadir = "./data"
logdir = "./log"
reportdir = "./report"
datafile = "BTC_USDT_1h.csv"      #!NOTICE: use our data "BTC_USDT_1h.csv" here
from_datetime = "2020-01-01 00:00:00"
to_datetime = "2020-04-01 00:00:00"


# %%
class OptDoubleSMACross(bt.Strategy):
    params = (
        ("pfast", 10),
        ("pslow", 20),
    )

    def log(self, txt, dt=None, doprint=False):     #(by default don't print log here)
        if doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print("%s, %s" % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close

        # add both "fast" and "slow" SimpleMovingAverage indicators
        self.fastsma = bt.indicators.SimpleMovingAverage(self.datas[0], period = self.params.pfast)
        self.slowsma = bt.indicators.SimpleMovingAverage(self.datas[0], period = self.params.pslow)
        # add a "CrossOver" signal!!
        self.crossover = bt.indicators.CrossOver(self.fastsma, self.slowsma) #NOTICE here passing in "fast" SMA as 1st line, "slow" SMA as 2nd line
        #["CrossOver" indicator Usage reference: https://www.backtrader.com/home/helloalgotrading/; documentation: https://www.backtrader.com/docu/indautoref/#crossover]
    
    def next(self):

        if not self.position:         #if not in the market yet (no "position" yet)
            if self.crossover > 0:     # "CrossOver" function return 1.0: meaning "fast SMA"(1st line) crosses the "slow SMA"(2nd line) upwards
                #--BUY!
                self.buy()
        else:           #("already in the market")
            if self.crossover < 0:     #"CrossOver" function return -1.0: meaning "fast SMA"(1st line) crosses the "slow SMA"(2nd line) downwards
                #--SELL!
                self.sell()

    #*** added "Strategy hook" here - "stop" method, in order to record the portfolio final net value of each optimization round:  
    def stop(self):
        self.log("Fast SMA Period %2d, Slow SMA Period %2d: Ending Value %.2f" %
        (self.params.pfast, self.params.pslow, self.broker.getvalue()), doprint=True)   #(do print the log message by the end of each optimization round here)
      


# %%
if __name__ == "__main__":
    cerebro = bt.Cerebro()

    # feed data:
    data = pd.read_csv(os.path.join(datadir, datafile), index_col="datetime", parse_dates=True)
    data = data.loc[(data.index >= pd.to_datetime(from_datetime)) & (data.index <= pd.to_datetime(to_datetime))]         #(just in case for the chosen time window here)
    datafeed = bt.feeds.PandasData(dataname=data, timeframe=bt.TimeFrame.Minutes, compression=60)                 #***! NOTICE detail: specify the time frame as 'Hourly Data" as here
    cerebro.adddata(datafeed)

    # add an "optimization strategy"
    strats = cerebro.optstrategy(OptDoubleSMACross, pfast=range(5,21), pslow=range(10,51))  #optimizing grid here: "pfast" parameter from 5 to 20 & "pslow" parameter from 10 to 50

    cerebro.addsizer(bt.sizers.PercentSizer, percents=99)

    cerebro.broker.setcash(10000)
    cerebro.broker.setcommission(commission=0.001)

    cerebro.run(maxcpus=1)


# %%



