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
import etherscan.contracts as contracts
import json
import pandas as pd
import numpy as np

# %% [markdown]
# #### get contract ABI (and save the JSON formatted result in a csv file)

# %%
with open("/Users/baixiao/Desktop/caw-quant-training/section1/task3/api_key.json", mode='r') as key_file:
    key = json.loads(key_file.read())['key']
print(key)

address = '0xfb6916095ca1df60bb79ce92ce3ea74c37c5d359'


# %%
def get_contract_abi(address, key):
    api = contracts.Contract(address=address, api_key=key)
    abi = json.loads(api.get_abi())
    abi = pd.DataFrame(abi)
    abi.to_csv("./contract_abi.csv", index=False)

get_contract_abi(address, key)    #can pass in other address and key

# %% [markdown]
# #### get and save contract source code (in Solidity language)

# %%
def get_contract_sourcecode(address, key):
    api = contracts.Contract(address=address, api_key=key)
    sourcecode = api.get_sourcecode()
    outF = open("./contract_source_code.sol", "w")
    outF.write(sourcecode[0]['SourceCode'])
    outF.close()

get_contract_sourcecode(address, key)


# %%



