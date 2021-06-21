#!/usr/bin/env python3

import datetime
import time

import bcrypt
import pymysql.cursors

from utils import *

time.strftime("%Y-%m-%d %H:%M:%S")


class Connection:
    def __init__(self):
        self.db_conn = None
        self.connect()

    def __del__(self):
        if self.db_conn:
            self.db_conn.close()

    def connect(self):
        self.db_conn = pymysql.connect(host='localhost',
                                       user='chatbot',
                                       password='ChatbotTest',
                                       database='chatbot',
                                       cursorclass=pymysql.cursors.DictCursor)

    def login(self, user_name: str, password) -> int:
        with self.db_conn.cursor() as cursor:
            sql = "SELECT * FROM `Users` WHERE `user_name`=%s"
            cursor.execute(sql, (user_name, ))
            result = cursor.fetchone()
        if (result and bcrypt.checkpw(password.encode(),
                                      result["password_hash"].encode())):
            return result["user_id"]
        return None

    def add_user(self, user_name: str, password: str,
                 birth_date: datetime.date = None) -> int:
        birth_date = f"'{str(birth_date)}'" if birth_date is not None else "NULL"
        with self.db_conn.cursor() as cursor:
            sql = ("INSERT INTO `Users`(`user_name`, `password_hash`,"
                   "`signup_time`, `birth_date`) VALUES (%s,%s,NOW(),"
                   f"{birth_date})")
            cursor.execute(sql, (user_name, bcrypt.hashpw(password.encode(),
                                                          bcrypt.gensalt())))
        self.db_conn.commit()
        return self.get_user_data_by_username(user_name)["user_id"]

    def get_user_data_by_username(self, user_name):
        with self.db_conn.cursor() as cursor:
            sql = "SELECT * FROM `Users` WHERE `user_name`=%s"
            cursor.execute(sql, (user_name, ))
            result = cursor.fetchone()
        return result

    def get_user_data_by_id(self, user_id):
        with self.db_conn.cursor() as cursor:
            sql = "SELECT * FROM `Users` WHERE `user_id`=%s"
            cursor.execute(sql, (user_id, ))
            result = cursor.fetchone()
        return result

    def create_db(self):
        try:
            with self.db_conn.cursor() as cursor:
                sql = "SELECT * FROM Users"
                cursor.execute(sql)
                result = cursor.fetchone()
        except pymysql.err.ProgrammingError as e:
            if e.args[0] != pymysql.constants.ER.NO_SUCH_TABLE:
                raise e
        else:
            assert not result, error("Table Users exists and is empty")
            with self.db_conn.cursor() as cursor:
                sql = "DROP TABLE Users"
                cursor.execute(sql)
                self.db_conn.commit()

        with self.db_conn.cursor() as cursor:
            sql = ("CREATE TABLE Users ("
                   "    user_id INT UNSIGNED AUTO_INCREMENT,"
                   "    user_name TEXT UNIQUE COLLATE utf8_bin,"
                   "    password_hash TEXT,"
                   "    signup_date DATE NOT NULL,"
                   "    bith_date DATE NOT NULL,"
                   "    PRIMARY KEY (user_id)"
                   ");")
            cursor.execute(sql)
            self.db_conn.commit()


if __name__ == "__main__":
    print(debug("Creating (if not exists) database Users"))
    connection = Connection()
    connection.connect()
    connection.create_db()
