#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import sys
from datetime import datetime
from typing import Optional, Union, Dict

import requests
import pandas as pd

from onchain.utils import *


# In[2]:


# Setup Alchemy API and Session for makng requests

# os.environ['ALCHEMY_API_KEY'] = ''
alchemy_request_url = get_alchemy_request_url()
session = requests.Session()


# In[3]:


# Defining addresses that we want to query
input_addresses = [
    "0xBE5F037E9bDfeA1E5c3c815Eb4aDeB1D9AB0137B",
    "0xB033F13BB4F1cAF484AB5c090F22bE425b2146B3",
]


# In[4]:


# Getting the latest block for consistency in case
# the network moves to the next block while the script is running
latest_block = get_latest_block(alchemy_request_url, session)
latest_block = latest_block if latest_block else 'latest'


# In[5]:


balance_output = {}
transaction_history_output = {}
asset_count_summary_output = {}


# In[6]:


# Main Driver code
for address in input_addresses:
    # Validate input addresses. If an address is invalid,
    # skip to the next one that the user specified
    if not validate_input_address(address):
        print(f"Input string '{address}' is of the wrong format to be valid address! Skipping.")
        continue

    # If the address is valid, get it's ether balance at the latest block
    balance = get_balance(address, alchemy_request_url, session, block_num=latest_block)

    # Only continue with remainder of the logic if get_balance executes successfully
    if balance is None:
        print(f"get_balance() request failed for address {address}!")
        print("Continuing to next address")
        continue

    # Store the balance that we've computed
    balance_output[address] = balance

    # Get the transactions that were sent FROM the address
    transfers_from = get_transaction_history(
        address,
        alchemy_request_url,
        True,
        session,
        latest_block,
    )

    # Get the transactions that were sent TO the address
    transfers_to = get_transaction_history(
        address,
        alchemy_request_url,
        False,
        session,
        latest_block,
    )

    if transfers_to and not transfers_from:
        # If an address has been funded, but has made no "out" transactions

        # Convert the block number from hex to integer. Sort by block # descending.
        df_to = pd.DataFrame.from_dict(transfers_to)

        df_transaction_history = sanitize_transaction_history(df_to)

        # Get the current balance for each asset.
        df_asset_count = df_to.groupby('asset').sum('value')
        df_asset_count.fillna(0, inplace=True)

        df_asset_count.columns = ['current_balance']
    elif transfers_from and transfers_to:
        # If an address both has "from" and "to" transactions
        df_from = pd.DataFrame.from_dict(transfers_from)
        df_to = pd.DataFrame.from_dict(transfers_to)

        # Concatenate the "from" and "to" transactions into one dataframe
        df_transaction_history = pd.concat([df_from, df_to])
        df_transaction_history = sanitize_transaction_history(df_transaction_history)

        # Get the current balance for each asset for the "from" and "to" sets separately
        df_from_asset_count = df_from.groupby('asset').sum('value')
        df_to_asset_count = df_to.groupby('asset').sum('value')

        # Join these results together and compute the current balance
        # by subtracting the "from" values from the "to" values
        df_asset_count = df_to_asset_count.merge(df_from_asset_count, on = 'asset', how='outer')
        df_asset_count.columns = ['to_balance', 'from_balance']
        df_asset_count.fillna(0, inplace=True)

        df_asset_count['current_balance'] = df_asset_count['to_balance'] - df_asset_count['from_balance']
        df_asset_count.drop(columns = ["to_balance", "from_balance"], inplace=True)
    else:
        # If both API calls return None or empty list
        # If the address doesn't have any "to" transactions, can't happen
        print(f"Transaction history parsing for address {address} failed! Continuing.")
        continue

    # Drop NFT metadata columns.
    # ERC721 tx will stil appear in the output dataframe, but the count
    # will not be correct without doing some additional parsing.
    df_transaction_history = df_transaction_history.drop(['erc721TokenId', 'erc1155Metadata', 'tokenId'], axis = 1)

    # Remove tokens that the address may have held in the past but now has a 0 balance.
    # Remove exotic "migrate" transactions (see note about gOHM in README)
    df_asset_count = df_asset_count.loc[(df_asset_count > 0).any(axis=1)]

    # Set ETH current balance to previously computed balance value,
    # necessary without having to compute gas for all transactions
    df_asset_count[df_asset_count.index == 'ETH'] = balance_output[address]


    # Store the transaction history and asset count summary that we've computed
    transaction_history_output[address] = df_transaction_history
    asset_count_summary_output[address] = df_asset_count


# In[7]:


# Print output
if len(asset_count_summary_output) == 0:
    print('No summaries available!')
else:
    for valid_address in asset_count_summary_output:
        print(f"Printing transaction summary for address: {address} as of block {latest_block}\n")
        print(f"It's current balance is \n{balance_output[valid_address]} ether\n")
        print(f"It's current ERC20 token (and ETH) balance is {asset_count_summary_output[valid_address]}\n")
        print(f"This address had {len(transaction_history_output[valid_address])} transactions in total (completed + failed)\n")
        print(f"Here are the 5 most recent transactions:\n{transaction_history_output[valid_address].head()}\n")
        print("-"*90)


# ## Examples from Etherscan
# https://etherscan.io/address/0xbe5f037e9bdfea1e5c3c815eb4adeb1d9ab0137b
# https://etherscan.io/address/0xB033F13BB4F1cAF484AB5c090F22bE425b2146B3

# In[ ]:




