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
class TestStrategy(bt.Strategy):
    params = (
        ("maperiod", 15),
        ("printlog", False),          #(by default, the parameter defines here "no printing log")
    )

    def log(self, txt, dt=None, doprint=False):     #(by default don't print log here)
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print("%s, %s" % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close

        self.order = None      #(just for keeping track of pending order here)
        self.buyprice = None
        self.buycomm = None

        # add a SimpleMovingAverage indicator
        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period = self.params.maperiod)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log("BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm: %.2f" %
                (order.executed.price, order.executed.value, order.executed.comm))
            
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log("SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm: %.2f" %
                (order.executed.price, order.executed.value, order.executed.comm))

            self.bar_executed = len(self)
            
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order Canceled/Margin/Rejected")

        self.order = None     #(*Remember to MARK that "there's no more pending order now"!!!)

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log("OPERATION PROFIT, GROSS %.2f, NET %.2f" % (trade.pnl, trade.pnlcomm))
    
    def next(self):
        self.log("Close, %.2f" % self.dataclose[0])

        if self.order:         #(*"If there's still order pending!!" - don't do anything)
            return

        if not self.position:         #if not in the market yet (no "position" yet)
            if self.dataclose[0] > self.sma[0]:
                #BUY!
                self.log("BUY CREATE, %.2f" % self.dataclose[0])
                self.order = self.buy()
        else:           #("already in the market")
            if self.dataclose[0] < self.sma[0]:
                #SELL!
                self.log("SELL CREATE, %.2f" % self.dataclose[0])
                self.order = self.sell()

    #*** added "Strategy hook" here - "stop" method, in order to record the portfolio final net value of each optimization round:  
    def stop(self):
        self.log("(MA Period %2d) Ending Value %.2f" %
        (self.params.maperiod, self.broker.getvalue()), doprint=True)   #**parameter passed into the "self.log" method to PRINT the log message by the end of each optimization round here!!
      


# %%
if __name__ == "__main__":
    cerebro = bt.Cerebro()

    #*** add an "optimizing strategy" object!!!
    strats = cerebro.optstrategy(TestStrategy, maperiod=range(10, 31))      #***optimizing "grid" here: parameter "maperiod" value ranges from 10 to 31 (one by one)

    #!!! WARNING: REVISE THE "data" PATH CODE BELOW!!!!!
    datapath = "./data/orcl-1995-2014.txt"

    data = bt.feeds.YahooFinanceCSVData(
        dataname = datapath,
        fromdate = datetime.datetime(2000, 1, 1),
        todate = datetime.datetime(2000, 12, 31),
        reverse = False)          #("reverse=False": the data file already in ascending date order)

    cerebro.adddata(data)

    cerebro.broker.setcash(1000.0)
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    cerebro.broker.setcommission(commission=0.0)

    cerebro.run(maxcpus=1)          #* "maxcpus" parameter for "cerebro.run()" function": how many cores to use simultaneously for optimization (default "None" - all available cores)


# %%



