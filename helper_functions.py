import re
import sqlite3
from datetime import datetime


def init_db():
    conn = sqlite3.connect('signal_core.db')
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys = ON;')
    c.execute('PRAGMA journal_mode = WAL;')
    with open('Signal_core.sql') as f:
        data = f.read()
        c.executescript(data)
    c.execute('PRAGMA user_version = 1;')
    conn.commit()
    conn.close()

class DatabaseContextManager:

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        c = self.conn.cursor()
        c.execute('PRAGMA foreign_keys = ON;')
        c.execute('PRAGMA journal_mode = WAL;')
        c.execute('PRAGMA synchronous = NORMAL;')
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()
#date type for argparse

date_re=re.compile(r'^\d{2}-\d{2}-\d{4}$')
def date_type(s: str):
    s=s.strip().replace('/','-')
    if date_re.match(s):
        try:
            date=datetime.strptime(s, '%d-%m-%Y')
        except ValueError:
            raise ValueError(f"{s} is not a valid date")

    else:
        raise ValueError ("date format error (please use DD-MM-YYYY format)")
    return date

time_re=re.compile(r'^\d{2}:\d{2}$')
def time_type(s: str):
    s=s.strip().replace('.',':').replace(' ',':')
    if time_re.match(s):
        try:
            time=datetime.strptime(s, '%H:%M')
        except ValueError:
            raise ValueError(f"{s} is not a valid time")
    else:
        raise ValueError ("time format error (please use HH:MM 24hr format)")
    return time

def split_by_length_and_preceding_space(string):
    segments=[]
    current_start=0
    while current_start<len(string):
        potential_length=current_start+80
        split_point=0
        if potential_length>len(string):
            segments.append(string[current_start:])
            break
        if string[potential_length]==' ':
            split_point=potential_length
        else:
            for i in range(potential_length-1,current_start,-1):
                if string[i]==' ':
                    split_point=i
                    break
        segments.append(string[current_start:split_point].strip())
        current_start=split_point+1
    return segments


