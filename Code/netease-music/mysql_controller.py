# coding=utf-8
"""
This file work for controlling mysql
"""

from datetime import datetime
import mysql.connector


class MysqlController(object):
    """
    This is a class for controlling mysql
    """

    def __init__(self, user, password, database, host='127.0.0.1', port=3306):
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.port = port
        self.db_connection = self.establish_db_connection()

    def establish_db_connection(self):
        """
        Establish mysql connection.
        Return: connection
        """
        self.connect_time = datetime.now()
        return mysql.connector.connect(user=self.user, password=self.password, database=self.database, host=self.host, port=self.port)

    def dispose_db_connection(self):
        """
        Close db connection
        """
        if self.db_connection != None:
            self.db_connection.close()

    def sql_write(self, sql, params_list=None):
        """
        Execute sql. For write.
        """
        cursor = None
        connect = None
        try:
            connect = self.db_connection
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

    def sql_write_list(self, sql, params_list):
        """
        Execute sql. For write.
        """
        connect = None
        cursor = None
        row_num = 0
        try:
            connect = self.db_connection
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

    def sql_read(self, sql, params_list=None):
        """
        Execute sql. For read.
        """
        connect = None
        cursor = None
        try:
            connect = self.db_connection
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


if __name__ == '__main__':
    pass