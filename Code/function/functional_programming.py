"""This is a functional programming code"""

from fibonacci_sequence import fib

class Calculator(object):
    """This is a calculator"""

    def __init__(self):
        return

    def fibonacci(self, number):
        """This is the fibonacci dequence"""
        print('fibonacci 1')
        return fib(number)

    def fibonacci2(self, number, function):
        """This is functional fibonacci"""
        print('fibonacci 2')
        return function(number)

    def fibonacci3(self):
        """This is return functional fibonacci"""
        print('fibonacci 3')
        return self.fibonacci

    def fibonacci4(self, number):
        """This is lambda functional fibonacci"""
        print('fibonacci 4')
        fib4 = lambda f: self.fibonacci(number)
        return fib4(number)

