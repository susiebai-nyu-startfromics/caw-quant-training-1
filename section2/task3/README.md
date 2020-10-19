# Task3 Optimize Parameter in Strategy

In this task, you will learn how to optimize parameters in your strategy, calculate common used KPIs and select the **best** one out of the pool.

Although there are always debates when it comes to optimization and doing it **properly** is challenging, one should get his tools ready when he needs. Over-optimization is definitely data-mining and could be dangerous. However, ideas like dividing data into in-sample period and out-of-sample period, using a coarser gird search could help you, in the one hand, fit your model to data, and in the other hand, avoid over-fitting.

Before moving on, you should finish both section2/task1 and section2/task2, and get your reseach template and strategy code ready.

### 1. Read the Doc

Backtrader already supports strategy optimization, which is discussed in [Quick Start](https://www.backtrader.com/docu/quickstart/quickstart/#lets-optimize). The idea of cerebro.optstrategy is as simple as adding multiple strategies with different parameters like you do in cerebro.addstrategy.

1. run the code in Doc's Quick Start, play with it.
2. do the same thing but use SMACross(the double simple moving average crossover strategy you did in task2).

### 2. Calculate KPIs

Notice that in Doc's example, you're printing end value of each parameter combination. Then you will probably select the largest one for production.
Be careful, sometimes the **best** end-value parameter set in optimizing period might not be the **best** one to go.

How about adding more KPIs:

required:

- Return (EndValue / StartValue - 1)
- MaxDrawDown (Google "maximum drawdown" if you don't know)
- TotalTrades (Number of trades, = WinTrades + LossTrades )
- WinTrades (Number of win trades)
- LossTrades (Number of loss trades)
- WinRatio (WinTrades / TotalTrades)
- AverageWin$ (TotalWins dollar value / WinTrades)
- AverageLoss$ (TotalLosses dollar value / LossTrades)
- AverageWinLossRatio ( AverageWin$/AverageLoss$ )

optional:

- LongestWinStreak (Google Longest Win Streak if you don't know)
- LongestLossStreak (Same here)

desired output: [BTC_USDT_1h_SMACross.csv](./BTC_USDT_1h_SMACross.csv)

Format the output according to sample output above.

Hint: 
1. You may find some parts familiar if you did optional btreport part in task2. Check the source code to see how to caculate these KPIs.
2. You may refer to Backtrader Doc's [analyzer section](https://www.backtrader.com/docu/analyzers/analyzers/), or if you're interested in its [pyfolio](https://www.backtrader.com/docu/analyzers/pyfolio/) integration, or just do it yourself.

### 3. Select What You Prefer

Now you get a pool of different parameters and their KPIs to choose from. Then the selecting rule becomes customized.

If you are risky, you might take whatever strategy giving the most return, no matter how large the maxdrawdown is. However, if you don't like to loss, you might pick the one with highest win/loss ratio.

When it comes to multi-goals selection problems, the standard way is to assign weights to different KPIs, compute score, and select the one with highest one.

1. Compute rank of 4 KPIs:

- Rank of Return
- Rank of Maxdrawdown
- Rank of WinLossRatio
- Rank of AverageWinLossRatio 

Then, score = average of 4 Ranks, the smallest one is the winner. 