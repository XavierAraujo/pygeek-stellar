import unittest
from pygeek_stellar.utils.generic import *


class GenericTest(unittest.TestCase):

    def test_is_float_str(self):
        self.assertTrue(is_float_str('10.1'))
        self.assertTrue(is_float_str('-100.1'))
        self.assertTrue(is_float_str('-333'))
        self.assertTrue(is_float_str('20203.7814'))
        self.assertTrue(is_float_str('86762'))
        self.assertFalse(is_float_str('10,1'))
        self.assertFalse(is_float_str('10,1aa'))
        self.assertFalse(is_float_str('ten'))
        self.assertFalse(is_float_str('10.1.2'))

    def test_is_int_str(self):
        self.assertTrue(is_int_str('10'))
        self.assertTrue(is_int_str('-100'))
        self.assertFalse(is_int_str('-333.21'))
        self.assertFalse(is_int_str('20203.7814'))
        self.assertFalse(is_int_str('20203,7814'))
        self.assertFalse(is_int_str('101aa'))
        self.assertFalse(is_int_str('ten'))

    def test_is_in_range(self):
        self.assertTrue(is_in_range(10, 10, 20))
        self.assertTrue(is_in_range(15, 10, 20))
        self.assertTrue(is_in_range(20, 10, 20))
        self.assertFalse(is_in_range(9, 10, 20))
        self.assertFalse(is_in_range(21, 10, 20))
        self.assertFalse(is_in_range(-15, 10, 20))

        self.assertTrue(is_in_range(232.12, 232.12, 233.12))
        self.assertTrue(is_in_range(232.5, 232.12, 233.12))
        self.assertTrue(is_in_range(233.12, 232.12, 233.12))
        self.assertFalse(is_in_range(232.119, 232.12, 233.12))
        self.assertFalse(is_in_range(233.12001, 232.12, 233.12))

    def test_is_successful_http_status_code(self):
        self.assertTrue(is_successful_http_status_code(200))
        self.assertTrue(is_successful_http_status_code(299))
        self.assertTrue(is_successful_http_status_code(250))
        self.assertFalse(is_successful_http_status_code(199))
        self.assertFalse(is_successful_http_status_code(300))
        self.assertFalse(is_successful_http_status_code(400))

    def test_decode_json_content(self):
        pass
        # TODO


if __name__ == '__main__':
    unittest.main()
