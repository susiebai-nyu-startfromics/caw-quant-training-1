# Task2 Get market data from Binance

In task1, you learned how to download data from data sources like [CryptoCompare](https://www.cryptocompare.com/). While CryptoCompare is free with good data quality, sometimes you do need to get market data directly from crypto-exchanges, especially when you're trading.

This task will guide you to get data from [Binance](https://www.binance.com/en), one of the top crypto-exchanges.

## 1. Explore Binance Data API

[Binance API Documentation](https://binance-docs.github.io/apidocs/spot/en/#change-log)

[Binance Github Homepage](https://github.com/binance-exchange)

[Binance REST/WebSocket endpoints](https://github.com/binance-exchange/binance-official-api-docs)

[Binance Python SDK](https://github.com/binance-exchange/python-binance)

Binance provides two market categories: **Spot Market** and **Future Market**(you will be focusing on spot market), two data types: **Public Data** and **Private Data**.(public data is open to anyone with some constraints associated, while private data contains information like account balance, trade history, which requires you to have an account in Binance to access)

### Required

#### 1. **Use Binance Python SDK** to get public data

The worst case is, you don't have SDK(Software Development Kit) for the language you use, and have to deal with http request like what you did in task1. Fortunately, we have one this time. Using SDK will save you a lot of work since it has already done those tedious work for you.

**Write a script (.py file)**

- [ ] get candle data(aka kline, histo)
- [ ] get transactions(aka trades)
- [ ] get market depth(aka orderbook)

Format the data the way you like using pandas, save them seperately as csv.

Hint:

1. check its sdk repo: https://github.com/binance-exchange/python-binance, take a look at examples and source codes (client.py), you might find something similar to what you've done in task1(if you did the optional task). Find the specific endpoint you need.

2. Note that you don't need a api key to get public data.

### Optional

#### 1. Trade in Binance by its python SDK

- [ ] setup a binance account
- [ ] setup its trading api(you need to create a api key, api secret pair to trade)
- [ ] check python SDK, create a test order.

Note:

1. You don't need to have money in your account to create a test order.
2. Of course, You can put some money in it and create a real order, starting your life as a quantitative trader.
