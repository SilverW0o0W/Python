#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: Silver (silver.codingcat@gmail.com)
@create: 2022/8/31
@brief: 装饰器实现
"""


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class Test(object):
    def __init__(self, index):
        self.index = index
