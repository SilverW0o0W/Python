#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: Silver (silver.codingcat@gmail.com)
@create: 2022/8/30
@brief: __new__方法实现
"""


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance


class Test(Singleton):
    def __init__(self, index):
        self.index = index
