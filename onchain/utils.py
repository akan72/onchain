"""
Utility functions for securing project keys, parsing data etc.
"""

import os
import sys
from typing import Optional

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
