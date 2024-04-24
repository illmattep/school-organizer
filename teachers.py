from config import settings
from flask_sqlalchemy import SQLAlchemy
from flask_paginate import Pagination, get_page_parameter

class teachermanager:
    def __init__(self):
        self.language = settings.LANGUAGE
        self.c = settings.c
        self.conn = settings.conn

        self.c.execute('''CREATE TABLE IF NOT EXISTS teachers (
                id INTEGER PRIMARY KEY,
                name TEXT,
                surname TEXT,
                subjects TEXT)''')
        self.conn.commit()

        if settings.DEBUG:
            self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='teachers'")
            if self.c.fetchone():
                print("The 'teachers' table is working.")
            else:
                print("Failed to create the 'teachers' table.")

    def create_teacher(self, name, surname, subjects):
        self.c.execute("INSERT INTO teachers (name, surname, subjects) VALUES (?, ?, ?, ?, ?)", (name, surname, subjects))
        self.conn.commit()

    def delete_teacher(self, name):
        self.c.execute("DELETE FROM teachers WHERE name = ?", (name,))
        self.conn.commit()

    def get_teachers(self):
        self.c.execute("SELECT * FROM teachers")
        return self.c.fetchall()

    def print_teacher(self, teacher):
        name, surname, subjects = teacher
        print(f"Teacher {name} {surname} teaches {subjects}")

    def get_teacher_by_id(self, id):
        self.c.execute("SELECT * FROM teacher WHERE id = ?", (id,))
        return self.c.fetchone()
    

TeacherManagerobj = teachermanager()