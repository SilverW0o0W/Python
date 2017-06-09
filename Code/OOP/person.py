"""This is a person base class"""


class Person(object):
    """Persion : name, gender, age"""

    def __init__(self, name, gender, age):
        self.__name = name
        self.__gender = gender
        self.__age = age

    def get_name(self):
        """Get name value"""
        return self.__name

    def get_gender(self):
        """Get gender value"""
        return self.__gender

    def get_age(self):
        """Get age value"""
        return self.__age
