import unittest
from pygeek_stellar.utils.stellar import *


class StellarTest(unittest.TestCase):

    PUBLIC_KEY1 = 'GB3I37MLME4LC5LVAKRTKSKE2K7X5VR4MEBVG3EVHMB2C6V6J5A3XC6L'
    PRIVATE_KEY1 = 'SADGEOC6FE5KQJMC7O65HNURFZTB6SLJDM5JB665NSWOGVBEGRRGC3KK'

    PUBLIC_KEY2 = 'GA6S6WSZVDBJQFEGYPZO7D5HWQINTIOSCKR5PAJRGZ4ZI2H7HED6V5RX'
    PRIVATE_KEY2 = 'SDNYPEIU5OOKMPZESV3S7NCJDF32UCUTPTXOOXWYWAGOQVKRCSEPC7PR'

    def test_is_valid_public_key(self):
        self.assertTrue(is_valid_public_key(StellarTest.PUBLIC_KEY1))
        self.assertTrue(is_valid_public_key(StellarTest.PUBLIC_KEY2))
        self.assertFalse(is_valid_public_key(StellarTest.PRIVATE_KEY1))
        self.assertFalse(is_valid_public_key(StellarTest.PRIVATE_KEY2))
        self.assertFalse(is_valid_public_key('invalid_key'))
        self.assertFalse(is_valid_public_key(None))

    def test_is_valid_private_key(self):
        self.assertTrue(is_valid_private_key(StellarTest.PRIVATE_KEY1))
        self.assertTrue(is_valid_private_key(StellarTest.PRIVATE_KEY2))
        self.assertFalse(is_valid_private_key(StellarTest.PUBLIC_KEY1))
        self.assertFalse(is_valid_private_key(StellarTest.PUBLIC_KEY2))
        self.assertFalse(is_valid_private_key('invalid_key'))
        self.assertFalse(is_valid_private_key(None))

    def test_is_valid_transaction_text_memo(self):
        self.assertTrue(is_valid_transaction_text_memo(''))
        self.assertTrue(is_valid_transaction_text_memo('Salary Transaction'))
        self.assertTrue(is_valid_transaction_text_memo('x'*28))
        self.assertFalse(is_valid_transaction_text_memo('x'*29))
        self.assertFalse(is_valid_transaction_text_memo(None))

    def test_is_valid_keypair(self):
        self.assertTrue(is_valid_keypair(public_key=StellarTest.PUBLIC_KEY1,
                                         private_key=StellarTest.PRIVATE_KEY1))
        self.assertTrue(is_valid_keypair(public_key=StellarTest.PUBLIC_KEY2,
                                         private_key=StellarTest.PRIVATE_KEY2))
        self.assertFalse(is_valid_keypair(public_key=StellarTest.PUBLIC_KEY1,
                                          private_key=StellarTest.PRIVATE_KEY2))
        self.assertFalse(is_valid_keypair(public_key=StellarTest.PUBLIC_KEY1,
                                          private_key='invalid_key'))
        self.assertFalse(is_valid_keypair(public_key='invalid_key',
                                          private_key=StellarTest.PRIVATE_KEY1))
        self.assertFalse(is_valid_keypair(public_key=StellarTest.PUBLIC_KEY1,
                                          private_key=None))


if __name__ == '__main__':
    unittest.main()
