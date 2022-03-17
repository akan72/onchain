from re import S
import unittest
import pandas as pd

import onchain
from onchain.utils import (
    get_alchemy_request_url,
    is_hexadecimal,
    validate_input_address,
    get_balance,
    get_latest_block,
)

alchemy_request_url = get_alchemy_request_url()

vitalik_address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
class TestRunner(unittest.TestCase):
    "Unittesting script for testing the onchain project"

    # Utility Function Tests
    def test_is_hexadecimal_false(self):
        self.assertFalse(is_hexadecimal('test'))

    def test_is_hexadecimal_true(self):
        self.assertTrue(is_hexadecimal('01af'))

    def test_is_hexadecimal_true(self):
        self.assertTrue(is_hexadecimal('0x01af'))

    def test_validate_input_address_simple(self):
        self.assertIsNone(validate_input_address("test"))

    def test_validate_input_address_correct_length(self):
        address = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        self.assertTrue(validate_input_address(address))

    def test_validate_input_address_correct_length(self):
        address = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaz"
        self.assertIsNone(validate_input_address(address))

    def test_validate_input_address_vitalik_no_prefix(self):
        res = validate_input_address(vitalik_address[2:])

        self.assertEqual(res, vitalik_address)

    def test_validate_input_address_vitalik_prefix(self):
        res = validate_input_address(vitalik_address)

        self.assertEqual(res, vitalik_address)

    # API Function Tests
    def test_get_latest_block(self):
        """"""
        self.assertIsInstance(get_latest_block(alchemy_request_url), str)

    def test_get_balance_malformed_address(self):
        """Testing get_balance with an invalid address"""
        res = get_balance("test", alchemy_request_url)
        self.assertIsNone(res)

    def test_get_balance_valid_address(self):
        """Testing get_balance with a valid address"""
        res = get_balance(vitalik_address, alchemy_request_url)
        self.assertIsInstance(res, float)

    def test_get_balance_malformed_block_number(self):
        """Testing get_balance with an block number"""
        res = get_balance(vitalik_address, alchemy_request_url, block_num = "0x-1")
        self.assertIsNone(res)

    # Program output tests
    def assert_output_type(self):
        """Test to ensure that the script output is a `pd.DataFrame`"""
        # self.assertIsInstance(..., pd.DataFrame)
        pass

    def assert_output_n_columns(self):
        """Test to ensure that the script output has the correct # of columns"""
        # self.assertIsInstance(..., pd.DataFrame)
        pass

if __name__ == "__main__":
    unittest.main()