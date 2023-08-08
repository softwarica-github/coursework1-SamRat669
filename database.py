import platform
import psutil
import sqlite3 as db
from datetime import date

connect = db.connect('data.db')
cursor = connect.cursor()
info = platform.system() + ' ' + str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + "GB"


def create_tables():
    # Create the "initial" table if it does not exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS initial (
        NAME TEXT,
        USERNAME TEXT PRIMARY KEY,
        PASSWORD TEXT,
        DATE_CREATED DATE
    )
    """)

    # Create the "user" table if it does not exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user (
        ID INTEGER PRIMARY KEY,
        FORMAT TEXT,
        TIME_STAMP DATE,
        FILE_PATH TEXT,
        PASSWORD TEXT,
        OS_RAM TEXT
    )
    """)

    connect.commit()


def new(name: str, user: str, passwd: str):
    cursor.execute("INSERT INTO initial VALUES (?, ?, ?, ?)", (name, user, passwd, date.today()))
    connect.commit()


def format_txt(file: str, passwd: str):
    cursor.execute("INSERT INTO user VALUES (?, ?, ?, ?, ?, ?)", ('text', date.today(), file, passwd, info))
    connect.commit()


def format_oth(types: str, file: str):
    cursor.execute("INSERT INTO user(FORMAT, TIME_STAMP, FILE_PATH, OS_RAM) VALUES (?, ?, ?, ?)", (types, date.today(), file, info))
    connect.commit()


def main_work(username: str, passwd: str, file: str):
    data = cursor.execute("SELECT NAME, PASSWORD FROM initial WHERE USERNAME=?", (username,)).fetchall()
    if not data:
        return 'No Admin Account',
    else:
        for i in range(len(data)):
            if passwd == data[i][1]:
                data2 = cursor.execute("SELECT PASSWORD FROM user WHERE FILE_PATH=?", (file,)).fetchone()
                if not data2:
                    return 'No such file',
                else:
                    return data[i][0], data2
            else:
                return 'Wrong Password',


def close():
    connect.close()
