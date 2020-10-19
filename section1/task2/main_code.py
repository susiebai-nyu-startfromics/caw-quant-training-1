# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# *IMPORTANT!:
# first install python-binance package (using "pip") into this anaconda environment:

# conda activate cryptoalgowheel
# /anaconda3/envs/cryptoalgowheel/bin/pip install python-binance


# %%
import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.tz import tzutc
import dateparser      #important datetime-related package used in "python-binance" SDK: https://dateparser.readthedocs.io/en/latest/ 

from binance.client import Client

# %% [markdown]
# ### Candle Data
# %% [markdown]
# *API method see "client.py" source code - starting line 673* <br>
# 
# **generally "OHLCV" kind of data result format (12 fields):** <br>
# Open time; <br>
# Open; <br>
# High; <br>
# Low; <br>
# Close; <br>
# Volume; <br>
# Close time; <br>
# Quote asset volume; <br>
# Number of trades; <br>
# Taker buy base asset volume; <br>
# Taker buy quote asset volume; <br>
# a_field_that_can_be_ignored
# 

# %%
def get_candle(symbol, interval_str, start_time, end_time=None):
    client = Client()
    result = client.get_historical_klines(symbol=symbol, interval=interval_str, start_str=start_time, end_str=end_time)     #return two dimensional lists with each row having 12 fields ("OHLCV" kind of data)
    result = np.array(result)
    result = result[:,:9]
    result = pd.DataFrame(result, columns=["OpenTime", "Open", "High", "Low", "Close", "Volume", "CloseTime", "QuoteAssetVol", "NumOfTrades"])
    result.OpenTime = result.OpenTime.astype("int").apply(lambda d: datetime.utcfromtimestamp(d/1000).strftime("%Y/%m/%d %H:%M:%S UTC"))       #convert "OpenTime" to time string format (notice that original UNIX timestamp is in milliseconds!)
    result.CloseTime = result.CloseTime.astype("int").apply(lambda d: datetime.utcfromtimestamp(d/1000).strftime("%Y/%m/%d %H:%M:%S UTC")) #convert "CloseTime" to time string format
    result = result[["OpenTime", "CloseTime", "Open", "High", "Low", "Close", "Volume", "QuoteAssetVol", "NumOfTrades"]]
    result.to_csv("/Users/baixiao/Desktop/histo_kline_data.csv", index=False)


# %%
get_candle("BNBBTC", Client.KLINE_INTERVAL_1HOUR, "1 day ago EDT")
#get_candle("NEOBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago EDT")

# %% [markdown]
# 
# %% [markdown]
# ### Transactions
# %% [markdown]
# #### aggregated trades list
# %% [markdown]
# *API method see "client.py" source code - line 539* <br>
# 
# **API return:** <br>
# Aggregate tradeId; <br>
# Price; <br>
# Quantity; <br>
# First tradeId; <br>
# Last tradeId; <br>
# Timestamp; <br>
# Was_the_buyer_the_maker?; <br>
# Was_the_trade_the_best_price_match?

# %%
def get_agg_trades(symbol, start_time=None, end_time=None, fromId=None):
    #convert user-input datetime string format into UNIX timestamp:
    if isinstance(start_time, str):
        start_time = int(dateparser.parse(start_time).timestamp()*1000)
    if isinstance(end_time, str):
        end_time = int(dateparser.parse(end_time).timestamp()*1000)

    client = Client()
    try:
        result = client.get_aggregate_trades(symbol=symbol, startTime=start_time, endTime=end_time, fromId=fromId)
        result = pd.DataFrame(result)
        result = result.rename(columns={"a":"agg_tradeId", "p":"price", "q":"quantity", "f":"first_tradeId", "l":"last_tradeId", "T":"timestamp", "m":"isBuyerMaker", "M":"isBestMatch"})
        result.timestamp = result.timestamp.apply(lambda d: datetime.utcfromtimestamp(d/1000).strftime("%Y/%m/%d %H:%M:%S UTC"))       #convert "timestamp" to time string format
        result = result[["timestamp", "agg_tradeId", "price", "quantity", "first_tradeId", "last_tradeId", "isBuyerMaker", "isBestMatch"]]
        result.to_csv("/Users/baixiao/Desktop/agg_trades.csv", index=False)
    except:
        print("Error: time between startTime and endTime passed in cannot exceed 1 hour here!!")


# %%
#get_agg_trades("BNBBTC", 1599411600000, 1599413400000)
#get_agg_trades("BNBBTC", 1599350400000, 1599411600000)  #(*)Error appearing

get_agg_trades("BNBBTC", "September 6, 2020 13:00 EDT", "September 6, 2020 13:30 EDT")

# %% [markdown]
# #### most recent grades (last 500)
# %% [markdown]
# *API method see "client.py" source code - line 477* <br>

# %%
def get_rct_trades(symbol):
    client = Client()
    result = client.get_recent_trades(symbol=symbol)
    result = pd.DataFrame(result)
    result = result.rename(columns={"qty":"quantity"})
    result.time = result.time.apply(lambda d: datetime.utcfromtimestamp(d/1000).strftime("%Y/%m/%d %H:%M:%S UTC"))       #convert "time" to time string format
    result = result[["time", "id", "price", "quantity", "isBuyerMaker", "isBestMatch"]]
    result.to_csv("/Users/baixiao/Desktop/latest_500_trades.csv", index=False)


# %%
get_rct_trades("NEOBTC")


# %%


# %% [markdown]
# ### Market Depth (get latest orderbook entries)
# %% [markdown]
# *API method see "client.py" source code - line 440* <br>

# %%
def get_orderbook(symbol, limit=500):
    client=Client()
    api_result = client.get_order_book(symbol=symbol, limit=limit)
    result=pd.DataFrame()
    result["bid_price"] = np.array(api_result["bids"])[:,0]
    result["bid_quantity"] = np.array(api_result["bids"])[:,1]
    result["ask_price"] = np.array(api_result["asks"])[:,0]
    result["ask_quantity"] = np.array(api_result["asks"])[:,1]
    result.index += 1
    result.to_csv("/Users/baixiao/Desktop/latest_orderbook.csv", index=True)


# %%
get_orderbook("NEOBTC")


# %%



