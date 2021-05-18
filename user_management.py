import datetime
import getpass

import pymysql

import database as db
from utils import *


class User:
    '''
    We want to drop dangerous data like password hashes as fast as
    possible so that is not storred here. 
    '''
    def __init__(self, user_id: int, user_name: str,
                 signup_time: datetime.datetime,
                 birth_date: datetime.date):
        self.user_id = user_id
        self.user_name = user_name
        self.signup_time = signup_time
        self.birth_date = birth_date

    @classmethod
    def from_id(cls, user_id):
        user_raw = db.get_user_data_by_id(user_id)
        return cls(user_raw["user_id"],
                   user_raw["user_name"],
                   user_raw["signup_time"],
                   user_raw["birth_date"])
        

def login():
    print(blue("Username: "), end="\033[33m")
    user_name = input()
    if (not (3 <= len(user_name) <= 16) or any(c not in ("abcdefghijklmnopqrstuvwxyz"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890") for c in user_name)):
        print(green("Invalid name, please try again..."))
        return login()
    elif db.get_user_data_by_username(user_name) == None:
        print(green("No user called \"{}\", please try again...".format(yellow(user_name))))
        return login()
    else:
        password = getpass.getpass("\033[0m" + blue("Password: ") + "\033[33m")
        print("\033[0m", end='')
        if (user_id := db.login(user_name, password)) == None:
            print(green("Something went wrong, please try again..."))
            return login()
        return User.from_id(user_id)
    
def register():
    print(blue("Username: "), end="\033[33m")
    user_name = input()
    if (not (3 <= len(user_name) <= 16) or any(c not in ("abcdefghijklmnopqrstuvwxyz"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890") for c in user_name)):
        print(green("Invalid name, please try again..."))
        register()
    elif db.get_user_data_by_username(user_name) != None:
        print(green("Name already taken, please try again..."))
        register()
    else:
        password = getpass.getpass("\033[0m" + blue("Password: ") + "\033[33m")
        print("\033[0m", end='')
        if getpass.getpass(blue("Password again: ") + "\033[33m") != password:
            print(green("Passwords not the same, please try again..."))
            register()
        else:
            db.add_user(user_name, password)

