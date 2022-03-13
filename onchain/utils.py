"""
Utility functions for securing project keys, parsing data etc.
"""

import os
import sys

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
            import config
            infura_project_id = config.INFURA_PROJECT_ID
        except AttributeError:
            print("INFURA_PROJECT_ID in config.py not set! Exiting.")

            sys.exit(0)

    print("Successfully found INFURA_PROJECT_ID!")

    infura_request_url = f"https://mainnet.infura.io/v3/{infura_project_id}"
    return infura_request_url

if __name__ == "__main__":
    get_infura_request_url()
