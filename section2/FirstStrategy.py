# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# Important: need to install "backtrader" package/module from PyPI first!

# first, activate cryptoalgowheel conda environment
# then: /anaconda3/envs/cryptoalgowheel/bin/pip install backtrader[plotting]


# %%
# *** IMPORTANT: need to install "PyQt5" package from PyPI in order to plot!!!

# first, activate cryptoalgowheel conda environment
# then: /anaconda3/envs/cryptoalgowheel/bin/pip install PyQt5


# %%
# ***** NOTICE: the "matplotlib" package in the running environment must be lower than version "3.2.2" (otherwise cannot plot)!!!

# %%
# The dataset used here is "orcl-2014.txt" from the "datas" folder of the Github repository.

# %%
from __future__ import (absolute_import, division, print_function, unicode_literals)

import backtrader as bt
import matplotlib
#import matplotlib.pyplot as plt
import PyQt5

import datetime
import os.path
import sys


# %%
print(bt.__version__)
print(matplotlib.__version__)


# %%
class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):      #standard log entry print format
        dt = dt or self.datas[0].datetime.date(0)
        print("%s, %s" % (dt.isoformat(), txt))

    def __init__(self):
        #keep a reference to the "close" Line object
        self.dataclose = self.datas[0].close

        self.order = None
    
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log("BUY EXECUTED, %.2f" % order.executed.price)
            elif order.issell():
                self.log("SELL EXECUTED, %.2f" % order.executed.price)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order Canceled / Margin / Rejected!")

        self.order = None      #signal no pending order now (after execution)

    def next(self):
        self.log("Close, %.2f" % self.dataclose[0])

        if len(self) == 5:  #Suppose we would have a first Buy on the 5th bar
            self.log("BUY CREATE, %.2f" % self.dataclose[0])
            self.order = self.buy()
        if len(self) == 10:  #Suppose we would then have a first Sell on the 10th bar
            self.log("SELL CREATE, %.2f" % self.dataclose[0])
            self.order = self.sell()


if __name__ == '__main__':
    cerebro = bt.Cerebro()

    cerebro.addstrategy(TestStrategy)

    #modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    #datapath = os.path.join(modpath, '../data/orcl-2014.txt')
    datapath = "../data/orcl-2014.txt"
    #print(modpath)
    print(datapath)

    data = bt.feeds.YahooFinanceCSVData(dataname=datapath, fromdate=datetime.datetime(2014, 1, 2), todate=datetime.datetime(2014, 12, 31), reverse=False)    #*! "reverse" parameter could be set to "False"(default "False") as the pre-downloaded YahooFinance format data has already the right ascending date order

    cerebro.adddata(data)
    cerebro.broker.setcash(100000.0)     #set initial balance in the trading account
    #Suppose: no Commission in this case

    print("Starting Portfolio Value: %.2f" % cerebro.broker.getvalue())

    cerebro.run()

    print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())
    
    #***!!!NOTICE use "Qt5Agg" matplotlib backend!!!
    matplotlib.use("Qt5Agg")
    #plt.switch_backend("Qt5Agg")
    cerebro.plot(height=30, iplot=False)
    #plt.show()

# %%
#another Test Strategy 
# (PyAlgoTrade example - using a Simple Moving Average indicator:
# - buy if the close is greater than the moving average
# - sell if the close is smaller than the moving average
#  - (*)only 1 active operation is allowed in the market):

class TestStrategy2(bt.Strategy):

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print("%s, %s" % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close

        self.order = None

        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=5)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log("BUY EXECUTED, Price: %.2f, Cost: %.2f, Stake: %.2f, Commission: %.2f" % (order.executed.price, order.executed.value, order.executed.size, order.executed.comm))
            else:
                self.log("SELL EXECUTED, Price: %.2f, Cost: %.2f, Stake: %.2f, Commission: %.2f" % (order.executed.price, order.executed.value, order.executed.size, order.executed.comm))

        elif order.status in [ord/er.Canceled, order.Margin, order.Rejected]:
            self.log("Order Canceled / Margin / Rejected")
        
        self.order = None       #remember to signal no pending order now

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        
        self.log("OPERATION PROFIT, GROSS %.2f, NET %.2f" % (trade.pnl, trade.pnlcomm))

    def next(self):
        self.log("Close, %.2f" % self.dataclose[0])
    
        if self.order:      #if there's a pending order, don't send a 2nd order
            return

        if not self.position:     #if not yet in the market! -- can only Buy first
            if self.dataclose[0] > self.sma[0]:      #if close greater than sma currently --buy!
                self.log("BUY CREATE, %.2f" % self.dataclose[0])
                self.order = self.buy()      #remember to signal there's a BUY pending order!   
        else:    #already in the market
            if self.dataclose[0] < self.sma[0]:      #if close smaller than sma currently -- sell!
                self.log("SELL CREATE, %.2f" % self.dataclose[0])
                self.order = self.sell()     #remember to signal there's a SELL pending order!
            
if __name__ == "__main__":
    cerebro = bt.Cerebro()

    cerebro.addstrategy(TestStrategy2)

    #modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    #datapath = os.path.join(modpath, "../data/orcl-2014.txt")
    datapath = "../data/orcl-2014.txt"
    #print(modpath)
    print(datapath)

    data = bt.feeds.YahooFinanceCSVData(dataname=datapath, fromdate=datetime.datetime(2014, 1, 2), todate=datetime.datetime(2014, 12, 31), reverse=False)

    cerebro.adddata(data)

    cerebro.broker.setcash(1000.0)

    cerebro.addsizer(bt.sizers.FixedSize, stake=10)      #10 'stake' now instead of default 1 'stake'

    cerebro.broker.setcommission(commission=0.0)      #mark the broker commission rate here

    print("Starting Portfolio Value: %.2f" % cerebro.broker.getvalue())

    cerebro.run()

    print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())

    #***!!!NOTICE use "Qt5Agg" matplotlib backend!!!
    matplotlib.use("Qt5Agg")
    cerebro.plot(height=30, iplot=False)


# %%



