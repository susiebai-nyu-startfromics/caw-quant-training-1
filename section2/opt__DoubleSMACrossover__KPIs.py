# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# first, REMEMBER to activate cryptoalgowheel-S2 environment!


# %%
import datetime
import os
import sys

import backtrader as bt
import backtrader.analyzers as btanalyzers
import numpy as np
import pandas as pd
import matplotlib
import PyQt5
import seaborn
import sklearn


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
    
        # *****! Warning: avoid the erroreous cases of "pslow" larger than "pfast"!
        # *** Documentation: https://www.backtrader.com/docu/exceptions/#strategyskiperror
        if self.params.pslow < self.params.pfast+5:
            raise bt.errors.StrategySkipError

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
      

# %% [markdown]
# KPIs to be calculated: <br>
# - Return (ending and starting values)
# - MaxDrawDown
# - TotalTrades (number of trades, WinTrades + LossTrades)
# - WinTrades
# - LossTrades
# - WinRatio (WinTrades / TotalTrades)
# - AverageWin$ (TotalWins dollar value / WinTrades)
# - AverageLoss$ (TotalLosses dollar value / LossTrades)
# - AverageWinLossRatio (AverageWin\$ / AverageLoss\$)

# %%
if __name__ == "__main__":
    cerebro = bt.Cerebro()

    # feed data:
    data = pd.read_csv(os.path.join(datadir, datafile), index_col="datetime", parse_dates=True)
    data = data.loc[(data.index >= pd.to_datetime(from_datetime)) & (data.index <= pd.to_datetime(to_datetime))]         #(just in case for the chosen time window here)
    datafeed = bt.feeds.PandasData(dataname=data, timeframe=bt.TimeFrame.Minutes, compression=60)                   #***! Notice detail: specify the time frame as "Hourly Data" as here
    cerebro.adddata(datafeed)

    # add an "optimization strategy"
    strats = cerebro.optstrategy(OptDoubleSMACross, pfast=range(5,21), pslow=range(10,51))  #optimizing grid here: "pfast" parameter from 5 to 20 & "pslow" parameter from ("pfast"+5) to 50
    #***IMPORTANT NOTICE of detail: "pslow" must be larger than "pfast"!!!(otherwise bugs)

    cerebro.addsizer(bt.sizers.PercentSizer, percents=99)

    cerebro.broker.setcash(10000)
    cerebro.broker.setcommission(commission=0.001)

    # [pending] ***** Add Analyzers!!!
    cerebro.addanalyzer(btanalyzers.TimeReturn, timeframe=bt.TimeFrame.NoTimeFrame, _name = "timereturn")
    cerebro.addanalyzer(btanalyzers.DrawDown, _name="drawdown")
    cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name="trade_comp")

    # add writer
    #cerebro.addwriter(bt.WriterFile, out="/Users/baixiao/Desktop/temp_opt.csv", csv=True)

    results = cerebro.run(maxcpus=1)          #[documentation: https://www.backtrader.com/docu/cerebro/#returning-the-results]

# %% [markdown]
# optimization documentation: https://www.backtrader.com/docu/optimization-improvements/

# %%
### Extract optimization analyzer results ("KPIs")
result_df = []
for i in range(len(results)):
    try:
        name = "SMACross"
        sma_pfast = results[i][0].params.__dict__["pfast"]
        sma_pslow = results[i][0].params.__dict__["pslow"]
        rtn = list(results[i][0].analyzers.timereturn.get_analysis().values())[0]
        maxdrawdown = results[i][0].analyzers.drawdown.get_analysis().max.drawdown
        totaltrades = results[i][0].analyzers.trade_comp.get_analysis().total.closed
        wintrades = results[i][0].analyzers.trade_comp.get_analysis().won.total
        losstrades = results[i][0].analyzers.trade_comp.get_analysis().lost.total
        winratio = wintrades / totaltrades
        averagewinvalue = results[i][0].analyzers.trade_comp.get_analysis().won.pnl.average
        averagelossvalue = results[i][0].analyzers.trade_comp.get_analysis().lost.pnl.average
        averagewinlossratio = abs(averagewinvalue / averagelossvalue)
        longestwinstreak = results[i][0].analyzers.trade_comp.get_analysis().streak.won.longest
        longestlossstreak = results[i][0].analyzers.trade_comp.get_analysis().streak.lost.longest
        current = {"Name": name, "sma_pfast": sma_pfast, "sma_pslow": sma_pslow, "Return": round(rtn, 4), "MaxDrawDown": round(maxdrawdown, 4), "TotalTrades#": totaltrades, "WinTrades#": wintrades, "LossTrades#": losstrades, "WinRatio": round(winratio, 4), "AverageWin$": round(averagewinvalue, 4), "AverageLoss$": round(averagelossvalue, 4), "LongestWinStreak": longestwinstreak, "LongestLossStreak": longestlossstreak, "AverageWinLossRatio": round(averagewinlossratio, 4)}
        result_df.append(current)
    except:        #*****! Warning: there're certain indexes where the strategy has been "skipped" ("bt.errors.StrategySkipError" set previously) -- "list index out of range" error would happen in these places!!!
        pass

result_df = pd.DataFrame(result_df)


# %%
result_df

# %% [markdown]
# #### Compute the ranks for 4 KPIs and calculate final score (average of 4 ranks)
# 
# (Notice!: here use "minimum rank" to be assigned to **ties**)
# %% [markdown]
# rank of 4 KPIs:<br>
# - rank of Return
# - rank of MaxDrawDown
# - rank of WinRatio
# - rank of AverageWinLossRatio

# %%
result_df["RankReturn"]=result_df["Return"].rank(method="min", ascending=False).astype("int")
result_df["RankMaxDrawDown"]=result_df["MaxDrawDown"].rank(method="min", ascending=True).astype("int")
result_df["RankWinRatio"]=result_df["WinRatio"].rank(method="min", ascending=False).astype("int")
result_df["RankAverageWinLossRatio"]=result_df["AverageWinLossRatio"].rank(method="min", ascending=False).astype("int")


# %%
result_df["Score"]= (result_df["RankReturn"]+result_df["RankMaxDrawDown"]+result_df["RankWinRatio"]+result_df["RankAverageWinLossRatio"])/4


# %%
result_df


# %%
#The Winner!:
result_df[result_df["Score"]==result_df["Score"].min()]


# %%
result_df.to_csv("./BTC_USDT_1h_SMACross.csv")


# %%



