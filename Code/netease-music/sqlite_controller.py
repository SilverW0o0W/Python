# coding=utf-8
"""
This is for controlling sqlite
"""

import threading

import os
import sqlite3


class SqliteController(object):
    """
    This is a class for controlling sqlite
    """
    __db_connection = None
    __db_min_storage = 10

    __sql_create_table = None
    __db_path = None

    def __init__(self, sql_create_table, db_path):
        self.__sql_create_table = sql_create_table
        self.__db_path = db_path
        self.init_db(sql_create_table)

    def init_db(self, sql_create_table=__sql_create_table):
        """
        Initialize sqlite db.
        """
        try:
            db_exist = os.path.exists(self.__db_path)
            self.__db_connection = self.establish_db_connection()
            if not db_exist:
                # Create db table
                return self.sql_write(sql_create_table)
            return True
        except sqlite3.DatabaseError:
            return False

    def establish_db_connection(self, check_thread=True):
        """
        Establish sqlite connection.
        Return: connection
        """
        return sqlite3.connect(self.__db_path, check_same_thread=check_thread)

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
        except sqlite3.DatabaseError, db_error:
            print db_error.message
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
                except sqlite3.DatabaseError:
                    continue
            connect.commit()
            return row_num
        except sqlite3.DatabaseError, db_error:
            print db_error.message
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
        except sqlite3.DatabaseError, db_error:
            print db_error.message
            return None
        finally:
            if cursor is not None:
                cursor.close()
            if is_main_thread is False and connect is not None:
                connect.close()
