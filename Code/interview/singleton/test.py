#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: Silver (silver.codingcat@gmail.com)
@create: 2022/8/31
@brief:
"""
import unittest


class TestSingletion(unittest.TestCase):
    def test1(self):
        from singleton_1 import Test as Test1
        a = Test1(1)
        b = Test1(2)
        self.assertIs(a, b)

    def test2(self):
        from singleton_2 import test
        a = test
        b = test
        self.assertIs(a, b)

    def test3(self):
        from singleton_3 import Test as Test3
        a = Test3(1)
        b = Test3(2)
        self.assertIs(a, b)

    def test4(self):
        from singleton_4 import Test as Test4
        a = Test4(1)
        b = Test4(2)
        # self.assertIs(a, b)


if __name__ == '__main__':
    unittest.main()
