# Task1 Get hourly candle data from CryptoCompare

[CryptoCompare](https://www.cryptocompare.com/) is a free cryptocurrency data source, where you can download market data, social media, news about cryptocurrencies. This task requires you to download data from CryptoCompare and do basic formatting.

## 1. Explore CryptoCompare Data API

[CryptoCompare Homepage](https://min-api.cryptocompare.com/)

[CryptoCompare Data API Documentation](https://min-api.cryptocompare.com/documentation)

### Required

#### 1. **Write a function** to download histohour data, parameters:

fsym: BTC, tsym: USDT, start_time="2017-04-01", end_time="2020-04-01", e='binance'

Hint:

1. check this url: https://min-api.cryptocompare.com/documentation?key=Historical&cat=dataHistohour

2. Learn how to do http request by python's [request](https://requests.readthedocs.io/en/master/user/quickstart/) library

3. Formatting downloaded data by [pandas](https://pandas.pydata.org/pandas-docs/stable/index.html), desired output example [BTC-USDT-1h.csv](./BTC_USDT_1h.csv)

4. You don't need api key for the two endpoints(get histohour data, get market cap toplist) in this task.

### Optional

#### 1. Modularize your code

**write a class** for CryptoCompare data api object and put your function into a member function.

#### 2. Add one more data endpoint

**write a member function** for one more endpoint, e.x. [Toplist by Market Cap Full Data](https://min-api.cryptocompare.com/documentation?key=Toplists&cat=TopTotalMktCapEndpointFull). (feel free to choose another one) and put it as another member function.
