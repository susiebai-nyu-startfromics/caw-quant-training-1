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
import etherscan.tokens as tokens
import json
import pandas as pd
import numpy as np


# %%
with open("/Users/baixiao/Desktop/caw-quant-training/section1/task3/api_key.json", mode='r') as key_file:
    key = json.loads(key_file.read())['key']
print(key)

#setting up the ERC20 token contract address (can be found by searching Etherscan.io for the coin wanted) here:
contract_address = '0x57d90b64a1a57749b0f932f1a3395792e12e7055'

# %% [markdown]
# #### get ERC20-Token Account Balance for an address given the token contract address

# %%
def ERC20token_account_bal(key, contract_address, address):
    api = tokens.Tokens(contract_address = contract_address, api_key=key)
    print(api.get_token_balance(address = address))

ERC20token_account_bal(key, contract_address, '0xe04f27eb70e025b78871a2ad7eabe85e61212761')

# %% [markdown]
# #### get ERC20-Token Total Supply given the token contract address

# %%
def ERC20token_total_supply(key, contract_adddress):
    api = tokens.Tokens(contract_address = contract_address, api_key=key)
    print(api.get_total_supply())

ERC20token_total_supply(key, contract_address)


# %%



