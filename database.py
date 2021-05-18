#!/usr/bin/env python3

import datetime
import time
import json

import bcrypt

import pymysql.cursors

time.strftime("%Y-%m-%d %H:%M:%S")

connection = pymysql.connect(host='localhost',
                             user='chatbot',
                             password='ChatbotTest',
                             database='chatbot',
                             cursorclass=pymysql.cursors.DictCursor)



def login(user_name: str, password) -> int:
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `Users` WHERE `user_name`=%s"
        cursor.execute(sql, (user_name, ))
        result = cursor.fetchone()
    if (result and
       bcrypt.checkpw(password.encode(), result["password_hash"].encode())):
       return result["user_id"]
    return None


def add_user(user_name: str, password: str,
             birth_date: datetime.date = None) -> int:
    birth_date = f"'{str(birth_date)}'" if birth_date != None else "NULL"
    with connection.cursor() as cursor:
        sql = ("INSERT INTO `Users`(`user_name`, `password_hash`,"
                "`signup_time`, `birth_date`) VALUES (%s,%s,NOW(),"
                f"{birth_date})")
        cursor.execute(sql, (user_name, bcrypt.hashpw(password.encode(),
                        bcrypt.gensalt())))
    connection.commit()
    return get_user_data_by_username(user_name)["user_id"]

def get_user_data_by_username(user_name):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `Users` WHERE `user_name`=%s"
        cursor.execute(sql, (user_name, ))
        result = cursor.fetchone()
    return result

def get_user_data_by_id(user_id):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `Users` WHERE `user_id`=%s"
        cursor.execute(sql, (user_id, ))
        result = cursor.fetchone()
    return result
