#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: Silver (silver.codingcat@gmail.com)
@create: 2022/8/31
@brief: 共享属性
"""


class Singleton(object):
    _attrs = {}

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        obj.__dict__ = cls._attrs
        return obj


class Test(Singleton):
    def __init__(self, index):
        self.index = index
