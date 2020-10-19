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
import etherscan.accounts as accounts
import json
import pandas as pd
import numpy as np
from datetime import datetime

# %% [markdown]
# ### single address

# %%
with open("/Users/baixiao/Desktop/caw-quant-training/section1/task3/api_key.json", mode='r') as key_file:
    key = json.loads(key_file.read())['key']
print(key)

address = '0x9dd134d14d1e65f84b706d6f205cd5b1cd03a46b'   #unique address for a transaction
# api = accounts.Account(address=address, api_key=key)

# %% [markdown]
# #### get balance

# %%
def get_bal(address, key):
    api = accounts.Account(address=address, api_key=key)
    print(api.get_balance())

get_bal(address,key)      
#get_bal(address='0xbb9bc244d798123fde783fcc1c72d3bb8c189413',key=key)

# %% [markdown]
# #### get a list of transactions by address

# %%
def get_trans_page(address, key, page=1, offset=10):
    api = accounts.Account(address=address, api_key=key)
    trans = api.get_transaction_page(page=page, offset=offset)     #(get paginated results here) ("offset" parameter: max records to return)
    trans = pd.DataFrame(trans)
    trans.timeStamp = trans.timeStamp.astype("int").apply(lambda d: datetime.utcfromtimestamp(d).strftime("%Y/%m/%d %H:%M:%S UTC"))
    trans.rename(columns={"timeStamp":"time"}, inplace=True)
    trans.to_csv("./normal_transactions.csv", index=False)

get_trans_page(address,key)              #you can pass in different address and key as parameters here


# %%
#!! Warning: seemingly "EmptyResponse" error from original API (in the case of "no transactions"?)

def get_all_trans(address, key):
    api = accounts.Account(address=address, api_key=key)
    api.get_all_transactions(offset=10000, sort='asc', internal=True)

get_all_trans(address,key)

# %% [markdown]
# #### collect "ERC20 Transactions"

# %%
def get_ERC20_trans(address, key):
    api = accounts.Account(address=address, api_key=key)
    ERC20trans = api.get_transaction_page(erc20=True)
    ERC20trans = pd.DataFrame(ERC20trans)
    ERC20trans.timeStamp = ERC20trans.timeStamp.astype("int").apply(lambda d: datetime.utcfromtimestamp(d).strftime("%Y/%m/%d %H:%M:%S UTC"))
    ERC20trans.rename(columns={"timeStamp":"time"}, inplace=True)
    ERC20trans.to_csv("./ETC20_transactions.csv", index=False)

get_ERC20_trans(address,key)

# %% [markdown]
# #### get a list of blocks mined by address

# %%
def get_block_mine_page(address, key):
    api = accounts.Account(address=address, api_key=key)
    blocks = api.get_blocks_mined_page(page=1, offset=10)
    blocks = pd.DataFrame(blocks)
    blocks.timeStamp = blocks.timeStamp.astype("int").apply(lambda d: datetime.utcfromtimestamp(d).strftime("%Y/%m/%d %H:%M:%S UTC"))
    blocks.rename(columns={"timeStamp":"time"}, inplace=True)
    blocks.to_csv("./blocks_mined.csv", index=False)

get_block_mine_page(address,key)

# %% [markdown]
# ### multiple addresses

# %%
addresses = ['0xbb9bc244d798123fde783fcc1c72d3bb8c189413', '0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a']

# %% [markdown]
# #### get balanaces of multiple addresses

# %%
def get_mul_account_bal(addresses, key):
    api = accounts.Account(address=addresses, api_key=key)
    mult_bal = pd.DataFrame(api.get_balance_multiple())
    mult_bal.to_csv("./balances_multiple_account.csv", index=False)

get_mul_account_bal(addresses, key)


# %%



