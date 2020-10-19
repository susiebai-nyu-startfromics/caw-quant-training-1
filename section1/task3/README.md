# Task3 Get on-chain data from Ethercan & news from CryptoControl

In task2, you learned how to download data by REST API or simply using SDK. We've covered third-party data source like [CryptoCompare](https://www.cryptocompare.com/) and crypto-exchange like [Binance](https://www.binance.com/en). There're two other types of data could be used by investment research purposes: on-chain data and news.

This task will guide you to get on-chain data from [Etherscan](https://etherscan.io/) and news from [CryptoControl](https://cryptocontrol.io/en/)

## 1. Explore Etherscan data API

[Etherscan API Documentation](https://etherscan.io/apis#misc)

[Etherscan Python SDK Github Homepage](https://github.com/corpetty/py-etherscan-api)

Etherscan provides on-chain data in ethereum network, including block, account, transaction, erc20 contract and etc. On-chain data is regarded as "fundamental" in crypto world with compared to financial statement in stock market. Google and do some research if you're not familiar with on-chain analysis.

### Required

#### 1. **Use Etherscan Python SDK** to get on-chain data

Explore examples and tests in [Etherscan Python SDK Repo](https://github.com/corpetty/py-etherscan-api), play with those endpoints, print and take a look at the data you can get and figure out what it means, and do some basic formating.

**Write some scripts (.py file)**

- [ ] play and combine scripts in examples/accounts
- [ ] play and combine scripts in examples/blocks
- [ ] play and combine scripts in examples/contracts
- [ ] play and combine scripts in examples/proxies
- [ ] play and combine scripts in examples/stats
- [ ] play and combine scripts in examples/tokens
- [ ] play and combine scripts in examples/transactions

Hint:

1. check its sdk repo: https://github.com/corpetty/py-etherscan-api, take a look at examples, tests and source codes. Find the specific endpoint you need.

### Optional

#### 1. learn Unittest in python

Unittest is normally used in software development regardless of programming language. Writing tests for your code not only makes it functionable and maintainable, but also clarifies its usage. Take a look at those tests in this repo: https://github.com/corpetty/py-etherscan-api/tree/master/tests.

Do some research on Google or maybe watch some videos in Youtube, learn:

1. Why write unittest code.
2. How to write unittests in python
3. How to setup unittest environment in your IDE (e.g. vscode)

Note:

1. There are 3 main unittest frameworks in python, unittest(built-in library), pytest and nose. Google them and compare, what are pros and cons?
2. Personally, I use pytest.

## 2. Explore CryptoControl data API

[CryptoControl API Documentation](https://cryptocontrol.io/en/developers/apis)

[CryptoControl Python SDK Github Homepage](https://github.com/cryptocontrol/python-api)

CryptoControl is one English free crypto-news provider. It covers
categoires like Analysis, Blockchain, Exchanges, General, Government, ICO and Mining news in crypto-world.

**Write a script (.py file)**

- [ ] play and explore all endpoints provided
- [ ] do some basic formating
