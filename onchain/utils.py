"""
Utility functions for securing project keys, parsing data etc.
"""

import os
import sys
from typing import Optional

import config


def get_infura_request_url() -> str:
    """Build the request URL for querying Infura either through an
    env variable or stored as a variable within config.py.

    Returns:
        Request URL used to query Infura's API
    """
    try:
        infura_project_id = os.environ["INFURA_PROJECT_ID"]
    except KeyError:
        print("INFURA_PROJECT_ID env variable not set! Trying from config.py.")

        try:
            infura_project_id = config.INFURA_PROJECT_ID
        except AttributeError:
            print("INFURA_PROJECT_ID in config.py not set! Exiting.")

            sys.exit(0)

    print("Successfully found INFURA_PROJECT_ID!")

    infura_request_url = f"https://mainnet.infura.io/v3/{infura_project_id}"
    return infura_request_url


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
        Sanitized address, or None if the input is not a valid address
    """

    # Trim leading "0x"
    if len(address) == 42 and address[0:2] == "0x":
        address = address[2:]

    if len(address) == 40:
        return is_hexadecimal(address)

    # TODO: Potentially an ENS address, can use the Web3 API for this
    print(f"'{address}' is not a valid address!")
    return None
