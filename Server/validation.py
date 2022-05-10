import os
import re
import sqlite3

path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(os.path.abspath(f"{path}/files/chat.db"))


def v_username(user: str):
    user = user.strip()
    query = f"SELECT usrUser from tblUser WHERE usrUser= ?"
    try:
        check_unique = conn.execute(query, (user,)).fetchone()[0]
        if check_unique == user:
            return "username is already used"
    except TypeError:
        if len(user) >= 5:
            return "OK"
        else:
            return "username must be at least 5 characters"


def v_Name(f_name, l_name):
    if len(f_name) >= 2 and len(l_name) >= 2:
        return "OK"
    else:
        return "first and last name must be at least 2 letters"


def v_email(email):
    query = f"SELECT usrEmail from tblUser WHERE usrEmail = ?"
    try:
        check_unique = conn.execute(query, (email,)).fetchone()[0]
        if check_unique == email:
            return "email is already used"
    except TypeError:
        if re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            return "OK"
        else:
            return "invalid email address"


def v_phone(phone: str):
    if len(phone) == 10 and phone.isdigit():
        return "OK"
    else:
        return "Phone number is too short"


def good_pass(inputString):
    return any(char.isdigit() for char in inputString) and any(char.isalpha() for char in inputString)


def v_pass(password):
    if len(password) < 8 or (not good_pass(password)):
        return "Password must be at least 8 characters with one letter and one digit"
    else:
        return "OK"
