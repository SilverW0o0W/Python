"""
This is Fibonacci sequence
"""

def fib(max_number):
    """This is Fibonacci sequence"""
    number, before, after = 0, 0, 1
    while number < max_number:
        yield after
        # temp = after
        # after = before + after
        # before = temp
        before, after = after, before + after
        number = number + 1
    return 'done'
