# coding=utf-8
"""
This is for controlling sqlite
"""

import os
import mysql.connector


class MysqlController(object):
    """
    This is a class for controlling sqlite
    """
    __db_connection = None
    __db_min_storage = 10

    def __init__(self, user, password, database):
        self.user = user
        self.password = password
        self.database = database
        self.init_db()

    def init_db(self):
        """
        Initialize sqlite db.
        """
        try:
            self.__db_connection = self.establish_db_connection()
            return True
        except StandardError, error:
            print error.message
            return False

    def establish_db_connection(self, check_thread=True):
        """
        Establish sqlite connection.
        Return: connection
        """
        return mysql.connector.connect(user=self.user, password=self.password, database=self.database)

    def dispose_db_connection(self):
        """
        Close db connection
        """
        if self.__db_connection != None:
            self.__db_connection.close()
            self.__db_connection = None

    def sql_write(self, sql, params_list=None, is_main_thread=True):
        """
        Execute sqlite sql. For write.
        """
        cursor = None
        connect = None
        try:
            if is_main_thread:
                connect = self.__db_connection
            else:
                connect = self.establish_db_connection(False)
            cursor = connect.cursor()
            if params_list is None:
                result = cursor.execute(sql)
            else:
                result = cursor.execute(sql, params_list)
            connect.commit()
            return result
        except StandardError, error:
            print error.message
            return None
        finally:
            if cursor is not None:
                cursor.close()
            if is_main_thread is False and connect is not None:
                connect.close()

    def sql_write_list(self, sql, params_list, is_main_thread=True):
        """
        Execute sqlite sql. For write.
        """
        connect = None
        cursor = None
        row_num = 0
        try:
            if is_main_thread:
                connect = self.__db_connection
            else:
                connect = self.establish_db_connection()
            cursor = connect.cursor()
            for params in params_list:
                try:
                    result = cursor.execute(sql, params)
                    row_num += result.rowcount
                except StandardError:
                    continue
            connect.commit()
            return row_num
        except StandardError, error:
            print error.message
            return None
        finally:
            if cursor is not None:
                cursor.close()
            if is_main_thread is False and connect is not None:
                connect.close()

    def sql_read(self, sql, params_list=None, is_main_thread=True):
        """
        Execute sqlite sql. For read.
        """
        connect = None
        cursor = None
        try:
            if is_main_thread:
                connect = self.__db_connection
            else:
                connect = self.establish_db_connection()
            cursor = connect.cursor()
            if params_list is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, params_list)
            result_set = cursor.fetchall()
            return result_set
        except StandardError, error:
            print error.message
            return None
        finally:
            if cursor is not None:
                cursor.close()
            if is_main_thread is False and connect is not None:
                connect.close()


if __name__ == '__main__':
    pass
