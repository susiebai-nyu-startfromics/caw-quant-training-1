# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
# ***Important: still, need to install "py-etherscan-api" package/module from PyPI first!

# first, activate cryptoalgowheel conda environment
# then: /anaconda3/envs/cryptoalgowheel/bin/pip install py-etherscan-api


# %%
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
import etherscan.stats as stats
import json
import pandas as pd
import numpy as np
from datetime import datetime


# %%
with open("/Users/baixiao/Desktop/caw-quant-training/section1/task3/api_key.json", mode='r') as key_file:
    key = json.loads(key_file.read())['key']
print(key)

# %% [markdown]
# #### get ETHER last price (and save result to a csv file)

# %%
def ether_last_price(key):
    api = stats.Stats(api_key=key)
    last_price = api.get_ether_last_price()
    last_price = pd.DataFrame(last_price, index=[0])
    last_price.ethbtc_timestamp = last_price.ethbtc_timestamp.astype("int").apply(lambda d: datetime.utcfromtimestamp(d).strftime("%Y/%m/%d %H:%M:%S UTC"))
    last_price.ethusd_timestamp = last_price.ethusd_timestamp.astype("int").apply(lambda d: datetime.utcfromtimestamp(d).strftime("%Y/%m/%d %H:%M:%S UTC"))
    last_price.rename(columns={'ethbtc_timestamp': 'ethbtc_time', 'ethusd_timestamp': 'ethusd_time'}, inplace=True)
    last_price = last_price[["ethbtc_time", "ethbtc", "ethusd_time", "ethusd"]]      #(order of cols)
    last_price.to_csv("./ethereum_last_price.csv", index=False)

ether_last_price(key)

# %% [markdown]
# #### get total supply of ETHER (in Wei)

# %%
def total_ether_supply(key):
    api = stats.Stats(api_key=key)
    print(api.get_total_ether_supply())

total_ether_supply(key)


# %%



