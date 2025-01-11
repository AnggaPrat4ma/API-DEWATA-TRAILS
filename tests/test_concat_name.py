import unittest

from helper.concat_name import concat_name

class TestConcatName(unittest.TestCase):
    def test_concat_name(self):
        self.assertEqual(concat_name("angga", "pratama"),  "angga pratama")
    def test_concat_name1(self):
        self.assertEqual(concat_name("gede", "pratama"),  "gede pratama")
    def test_concat_name2(self):
        self.assertNotEqual(concat_name("gede", "pratama"),  "gede   pratama")