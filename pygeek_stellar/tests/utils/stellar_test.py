import unittest
from pygeek_stellar.utils.stellar import *


class StellarTest(unittest.TestCase):

    ADDRESS_1 = 'GB3I37MLME4LC5LVAKRTKSKE2K7X5VR4MEBVG3EVHMB2C6V6J5A3XC6L'
    SEED_1 = 'SADGEOC6FE5KQJMC7O65HNURFZTB6SLJDM5JB665NSWOGVBEGRRGC3KK'

    ADDRESS_2 = 'GA6S6WSZVDBJQFEGYPZO7D5HWQINTIOSCKR5PAJRGZ4ZI2H7HED6V5RX'
    SEED_2 = 'SDNYPEIU5OOKMPZESV3S7NCJDF32UCUTPTXOOXWYWAGOQVKRCSEPC7PR'

    def test_is_valid_address(self):
        self.assertTrue(is_address_valid(StellarTest.ADDRESS_1))
        self.assertTrue(is_address_valid(StellarTest.ADDRESS_2))
        self.assertFalse(is_address_valid(StellarTest.SEED_1))
        self.assertFalse(is_address_valid(StellarTest.SEED_2))
        self.assertFalse(is_address_valid('invalid_key'))
        self.assertFalse(is_address_valid(None))

    def test_is_valid_seed(self):
        self.assertTrue(is_seed_valid(StellarTest.SEED_1))
        self.assertTrue(is_seed_valid(StellarTest.SEED_2))
        self.assertFalse(is_seed_valid(StellarTest.ADDRESS_1))
        self.assertFalse(is_seed_valid(StellarTest.ADDRESS_2))
        self.assertFalse(is_seed_valid('invalid_key'))
        self.assertFalse(is_seed_valid(None))

    def test_is_valid_transaction_text_memo(self):
        self.assertTrue(is_transaction_text_memo_valid(''))
        self.assertTrue(is_transaction_text_memo_valid('Salary Transaction'))
        self.assertTrue(is_transaction_text_memo_valid('x' * 28))
        self.assertFalse(is_transaction_text_memo_valid('x' * 29))
        self.assertFalse(is_transaction_text_memo_valid(None))

    def test_is_address_matching_seed(self):
        self.assertTrue(is_seed_matching_address(StellarTest.SEED_1, StellarTest.ADDRESS_1))
        self.assertTrue(is_seed_matching_address(StellarTest.SEED_2, StellarTest.ADDRESS_2))
        self.assertFalse(is_seed_matching_address(StellarTest.SEED_2, StellarTest.ADDRESS_1))
        self.assertFalse(is_seed_matching_address('invalid_key', StellarTest.ADDRESS_1))
        self.assertFalse(is_seed_matching_address('invalid_key', StellarTest.SEED_1))
        self.assertFalse(is_seed_matching_address(None, StellarTest.ADDRESS_1))


if __name__ == '__main__':
    unittest.main()
