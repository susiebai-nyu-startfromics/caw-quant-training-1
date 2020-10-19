# Task1 Backtest Framework Intro

In this task, you will learn how to use backtest framework to develop trading strategies. Backtest framework takes historical data, buying and selling logic to simulate real-world trades and compute capital gains or losses. There are plenty of open-source backtest framework available on [Github](https://github.com/search?q=backtest)

Popular librarys are [Backtrader](https://www.backtrader.com/), [vnpy](https://www.vnpy.com/), [Zipline](https://github.com/quantopian/zipline), and etc.

This task will guide you to use [Backtrader](https://www.backtrader.com/) to develop trading strategies.

## Required

### 1. Create a Seperate Repo and Virtual Environment

Set up a file structure in `section2/` like this to do all tasks:

```
section2
├── README.md
├── task1
│   └── README.md
├── task2
│   └── README.md
└── task3
│   └── README.md
└── data # folder to contain all data
│       BTC_USDT_1h
└── log # folder to contain all log files
│       logfile
└── report # folder to containe reports. e.x. photo and optmization table
│       reportfile
├── README.md
├── requirements.txt
├── your_script1.py
└── your_script2.py 
```

Note: 
1. Google **requirements.txt** if you don't know, what is it, why use it, how to create one. (python virtual environment is related)
2. It's good practice to create a virtual environment for every project you do. Google it if you don't know. 
3. Recommended virtual environment libraries: venv(built-in), conda, pipenv. I use anaconda based python, so I will go with conda. (Note: you can use conda as a package manager even if you don't use anaconda-based python)

### 2. Read the Doc and Example

[Backtrader Documentation](https://www.backtrader.com/docu/)

[Backtrader Repo](https://github.com/mementum/backtrader)

Backtrader is written elegantly by advanced OOP concepts like metaclass. It might feel difficult at the every beginning of learning it. However, the design pattern and ideas are worthy of spending some time diving into.


### 3. Write a Hello World Strategy

Use one of the [example data](https://github.com/mementum/backtrader/tree/master/datas), write a **script(.py file)**:

- [ ] use backtrader adddata to feed data.
- [ ] the strategy should have at least one buying and selling.
- [ ] use backtrader run to execute.
- [ ] use backtrader plot to visulize.

Hint:

1. Follow the [Quickstart Guide](https://www.backtrader.com/docu/quickstart/quickstart/)