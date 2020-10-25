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
from etherscan.proxies import Proxies
import json
import pandas as pd
import numpy as np
from datetime import datetime


# %%
with open("/Users/baixiao/Desktop/caw-quant-training/section1/task3/api_key.json", mode='r') as key_file:
    key = json.loads(key_file.read())['key']
print(key)


# %%
##### OOP:
class Proxies_usage:
    def __init__(self, key):
        self.api_key = key
        self.api = Proxies(api_key=key)

    #### get information about a block by block number (and save the result in a JSON file)
    def block_info_by_number(self, block_number):
        block = self.api.get_block_by_number(block_number)
        with open("./block_info_by_number.json", "w") as json_file:
            json.dump(block, json_file)
    
    #### get the number of transactions in a block matching the given block number
    def block_trans_count_by_number(self, block_number):
        tx_count = self.api.get_block_transaction_count_by_number(block_number = block_number)
        return int(tx_count, 16)

    #### get the number of most recent block
    def most_recent_block(self):
        block = self.api.get_most_recent_block()
        return int(block, 16)
    
    #### get information about a transaction by block number and transaction index position (and save to a csv file)
    def trans_info_by_number_index(self, block_number, index):
        transaction = self.api.get_transaction_by_blocknumber_index(block_number=block_number, index=index)
        transaction = pd.DataFrame(transaction, index=[0])
        transaction.to_csv("./transaction_info_by_number_index.csv", index=False)

    #### get the informationa bout a transaction by transaction hash (and save to a csv file)
    def trans_info_by_hash(self, hash):
        transaction = self.api.get_transaction_by_hash(tx_hash = hash)
        transaction = pd.DataFrame(transaction, index=[0])
        transaction.to_csv("./transaction_info_by_hash.csv", index=False)

    #### get the number of transactions sent from an address
    def trans_count_from_addr(self, address):
        count = self.api.get_transaction_count(address)
        return int(count, 16)

    #### get (display) the receipt of a transaction by transaction hash
    def trans_receipt_by_hash(self, hash):
        receipt = self.api.get_transaction_receipt(hash)
        receipt = pd.DataFrame.from_dict(receipt, orient="index")
        display(receipt)

    #### get information about a uncle by block number
    def uncle_by_number_index(self, block_number, index = "0x0"):
        uncles = self.api.get_uncle_by_blocknumber_index(block_number=block_number, index=index)
        return uncles["uncles"]


# %%
proxies = Proxies_usage(key)
proxies.block_info_by_number(5747732)
#print("transaction count:", proxies.block_trans_count_by_number("0x10FB78"))
print("transaction count:", proxies.block_trans_count_by_number("0x10FB78"))
print("most recent block:", proxies.most_recent_block())
proxies.trans_info_by_number_index(block_number = '0x57b2cc', index = '0x2')
proxies.trans_info_by_hash('0x1e2910a262b1008d0616a0beb24c1a491d78771baa54a33e66065e03b1f46bc1')
print("transaction count:", proxies.trans_count_from_addr('0x6E2446aCfcec11CC4a60f36aFA061a9ba81aF7e0'))
print("This is the transaction receipt below:")
proxies.trans_receipt_by_hash('0xb03d4625fd433ad05f036abdc895a1837a7d838ed39f970db69e7d832e41205d')
print("Uncles:", proxies.uncle_by_number_index(block_number = "0x210A9B"))


# %%



