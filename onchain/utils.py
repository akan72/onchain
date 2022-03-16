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
        alchemy_project_id = os.environ["ALCHEMY_PROJECT_ID"]
    except KeyError:
        print("ALCHEMY_PROJECT_ID env variable not set! Trying from config.py.")

        try:
            alchemy_project_id = config.ALCHEMY_PROJECT_ID
        except AttributeError:
            print("ALCHEMY_PROJECT_ID in config.py not set! Exiting.")

            sys.exit(0)

    print("Successfully found ALCHEMY_PROJECT_ID!")

    alchemy_request_url = f"https://eth-mainnet.alchemyapi.io/v2/{alchemy_project_id}"
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

    # Add "0x" prefix to hex addresses for consumption by Alchemy's APIs
    if len(address) == 40 and is_hexadecimal(address):
        return "0x" + address

    # Validate addresses already prefixed with "0x"
    if len(address) == 42 and address[0:2] == "0x" and is_hexadecimal(address[2:]):
        return address

    # TODO: Potentially an ENS address, can use the Web3 API for this
    print(f"'{address}' is not a valid address!")
    return None
