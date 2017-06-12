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

    def set_name(self, name):
        """Set name value"""
        self.__name = name

    def get_gender(self):
        """Get gender value"""
        return self.__gender

    def set_gender(self, gender):
        """Set gender value"""
        self.__gender = gender

    def get_age(self):
        """Get age value"""
        return self.__age

    def set_age(self, age):
        """Set age value"""
        self.__age = age
