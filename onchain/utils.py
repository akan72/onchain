"""
Utility functions for securing project keys, parsing data etc.
"""

import os
import sys
import requests
from typing import Optional, Union

from onchain import config

def get_alchemy_request_url() -> str:
    """Build the request URL for querying Alchemy either through an
    env variable or stored as a variable within config.py.

    Returns:
        Request URL used to query Alchemy's API
    """
    try:
        alchemy_api_key = os.environ["ALCHEMY_API_KEY"]
    except KeyError:
        print("ALCHEMY_API_KEY env variable not set! Trying from config.py.")

        try:
            alchemy_api_key = config.ALCHEMY_API_KEY
        except AttributeError:
            print("ALCHEMY_API_KEY in config.py not set! Exiting.")

            sys.exit(0)

    print("Successfully found ALCHEMY_API_KEY!")

    alchemy_request_url = f"https://eth-mainnet.alchemyapi.io/v2/{alchemy_api_key}"
    return alchemy_request_url


def is_hexadecimal(address: str) -> bool:
    """Determine if an input string is in hexadecimal format.
    Used for validating potential ETH addresses

    Args:
        address: String to check

    Returns:
        True if valid hex, else False
    """

    try:
        int(address, 16)
    except ValueError:
        return False
    return True


def validate_input_address(address: str) -> Optional[str]:
    """Determine if an input address is a validate Ethereum address

    Allowable formats:
        - Hexadecimal address only
        - Hexadecimal address prefixed by "0x"
        - TODO: ENS Address

    Args:
        address: String that may potentially be an Ethereum address

    Returns:
        Sanitized address prefixed by "0x", or None if the input is not a valid address
    """

    # Validate if addresses are in hexadecimal format
    if is_hexadecimal(address):
        # Add "0x" prefix to hex addresses for consumption by Alchemy's APIs if necessary
        if len(address) == 40:
            return "0x" + address

        if len(address) == 42:
            return address

    # TODO: Potentially an ENS address, can use the Web3 API for this
    print(f"'{address}' is not a valid address!")
    return None

def get_balance(address: str, alchemy_request_url: str, block_num: str = "latest"):
    """Get the current balance of an address in Ether
    """
    payload = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "eth_getBalance",
        "params": [
            address,
            block_num
        ]
    }

    response = requests.post(alchemy_request_url, json=payload)

    if response.status_code == 200:
        response = response.json()
        eth_result = convert_wei_to_ether(response['result'])

        print(f"Ether balance as of block {block_num} for address {address} is {eth_result} Ether")
        return eth_result
    else:
        print(f"Status code {response.status_code} returned when fetching balance for address {address}")

        response = response.json()
        if "error" in response:
            print(f"Error {response['error']}")
        return None


def convert_wei_to_ether(wei: Union[str, float]) -> float:
    """
    """
    if isinstance(wei, str) and is_hexadecimal(wei):
        decimal_wei = int(wei, 16)
        assert decimal_wei >=0

        return decimal_wei / (10**18)

    elif isinstance(wei, float):
        assert wei >= 0

        return wei / (10**18)