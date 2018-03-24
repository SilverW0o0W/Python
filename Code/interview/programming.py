# coding=utf-8

# Fibonacci sequence
# 1
fib = lambda n: n if n <= 2 else fib(n - 1) + fib(n - 2)


# 2
def memo(func):
    cache = {}

    def wrap(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return wrap


@memo
def fib(i):
    if i < 2:
        return 1
    return fib(i - 1) + fib(i - 2)


# 3
def fib(n):
    a, b = 0, 1
    for i in xrange(n):
        a, b = b, a + b
    return b

# 变态台阶
fib = lambda n: n if n < 2 else 2 * fib(n - 1)
