import sqlite3
import os
# Configuration class
class Config:
    def __init__(self):
        # Debug mode
        self.DEBUG = True

        # Language
        self.LANGUAGE = 'english' # Either 'english' or 'italiano'

        # Number of years
        self.NUM_YEARS = 5

        # Path to languages
        self.LANGUAGES_PATH = './languages'

        # List of class years
        self.CLASS_YEARS = list(range(1, self.NUM_YEARS + 1))

        # List of addresses
        self.ADDRESSES = [
            "Computer Science",
            "Electrical Engineering",
            "Mechanical Engineering",
        ]

        self.SUBJECTS = {
            'all_addresses': {
                'italian',
                'english',
                'math',
                'science',
                'history',
                'geography',
                'art',
                'music',
                'physical education',
                'computer science',
                'electrical engineering',
                'mechanical engineering',

            }
        }

        # Database connection
        self.db = 'school.db'
        self.conn = sqlite3.connect(self.db, check_same_thread=False) # Create a connection object
        self.c = self.conn.cursor() # Create a cursor object to execute SQL queries on the database 

settings = Config() # Get the configuration object modifiable by the user

