"""This is function result"""
from functional_programming import Calculator


__calculator__ = Calculator()
print(__calculator__.fibonacci(5))
print(__calculator__.fibonacci2(5, __calculator__.fibonacci))
__returnFib__ = __calculator__.fibonacci3()
print(__returnFib__(5))
print(__calculator__.fibonacci4(5))
