#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: Silver (silver.codingcat@gmail.com)
@create: 2022/8/29
@brief:
"""
import functools
import time


def print_time_without_input(func):
    def wrapper():
        t1 = time.time()
        func()
        t2 = time.time()
        print(t2 - t1)

    return wrapper


def print_time_with_input(func):
    def wrapper(a, b):
        t1 = time.time()
        r = func(a, b)
        t2 = time.time()
        print(t2 - t1)
        return r

    return wrapper


def print_time_with_params(print_out=True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(a, b):
            t1 = time.time()
            r = func(a, b)
            t2 = time.time()
            if print_out:
                print(t2 - t1)
            return r

        return wrapper

    return decorator


@print_time_without_input
def add_1():
    time.sleep(1)
    c = 1 + 2
    print(c)


@print_time_with_input
def add_2(a, b):
    time.sleep(1)
    return a + b


@print_time_with_params(print_out=True)
def add_3(a, b):
    time.sleep(1)
    return a + b


if __name__ == '__main__':
    # print(add_2(1, 3))
    print(add_3(4, 3))
