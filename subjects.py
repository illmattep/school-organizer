from config import settings
from flask_sqlalchemy import SQLAlchemy
from flask_paginate import Pagination, get_page_parameter

class subjectmanager:
    def __init__(self):
        self.language = settings.LANGUAGE
        self.c = settings.c
        self.conn = settings.conn

        self.c.execute('''CREATE TABLE IF NOT EXISTS subjects (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        address TEXT,
                        years TEXT,
                        needed_room TEXT,
                        preferred_room TEXT)''')
        self.conn.commit()


        if settings.DEBUG:
            self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='subjects'")
            if self.c.fetchone():
                print("The 'subjects' table is working.")
            else:
                print("Failed to create the 'subjects' table.")


    def create_subject(self, name, address, years, needed_room=None, preferred_room=None):
        self.c.execute("INSERT INTO subjects (name, address, years, needed_room, preferred_room) VALUES (?, ?, ?, ?, ?)", (name, address, years, needed_room, preferred_room))
        self.conn.commit()

    def delete_subject(self, name):
        self.c.execute("DELETE FROM subjects WHERE name = ?", (name,))
        self.conn.commit()

    def get_subjects(self):
        self.c.execute("SELECT * FROM subjects")
        return self.c.fetchall()

    def print_subject(self, subject):
        name, address, years, needed_room, preferred_room = subject
        print(f"Subject {name} is taught at {address} for years {years} and needs {needed_room} and prefers {preferred_room}")

    def get_subject_by_id(self, id):
        self.c.execute("SELECT * FROM subjects WHERE id = ?", (id,))
        return self.c.fetchone()
    

SubjectManagerobj = subjectmanager()