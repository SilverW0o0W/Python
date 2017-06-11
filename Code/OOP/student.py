"""This is person's child class"""

from person import Person


class Student(Person):
    """Student : school grade class id"""

    def __init__(self, name, gender, age, id, grade, class_number):
        Person.__init__(name, gender, age)
        self.__id = id
        self.__grade = grade
        self.__class = class_number

    def get_id(self):
        """Get id value"""
        return self.__id

    def get_grade(self):
        """Get grade value"""
        return self.__grade

    def get_class(self):
        """Get class value"""
        return self.__class
