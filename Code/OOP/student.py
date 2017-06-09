"""This is person's child class"""

from person import Person


class Student(Person):
    """Student : school grade class id"""

    def __init__(self, name, gender, age, id, grade, classNumber):
        Person.__init__(name, gender, age)
        self.__id = id
        self.__grade = grade
        self.__class = classNumber
