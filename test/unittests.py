import unittest
import pandas as pd

import onchain
from onchain.utils import (
    get_infura_request_url,
    is_hexadecimal,
    validate_input_address,
)

class TestRunner(unittest.TestCase):
    "Unittesting script for testing the onchain project"

    def test_is_hexadecimal_false(self):
        self.assertFalse(is_hexadecimal('test'))

    def test_is_hexadecimal_true(self):
        self.assertTrue(is_hexadecimal('01af'))

    def test_validate_input_address_simple(self):
        self.assertIsNone(validate_input_address("test"))

    def test_validate_input_address_vitalik(self):
        vitalik = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
        res = validate_input_address(vitalik)

        self.assertEquals(res, vitalik[2:])

    def test_1(self):
        """Test 1 Description"""
        pass

    def test_2(self):
        """Test 2 Description"""
        pass

    # def assert_output_type(self):
    #     """Test to ensure that the script output is a `pd.DataFrame`"""
    #     self.assertIsInstance(..., pd.DataFrame)

if __name__ == "__main__":
    unittest.main()