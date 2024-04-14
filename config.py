import sqlite3
# Configuration class
class Config:
    def __init__(self):
        # Language
        self.LANGUAGE = 'italiano' # Either 'english' or 'italiano'

        # Number of years
        self.NUM_YEARS = 5

        # List of class years
        self.CLASS_YEARS = list(range(1, self.NUM_YEARS + 1))

        # List of addresses
        if self.LANGUAGE == 'english':
            self.ADDRESSES = [
                "Computer Science",
                "Electrical Engineering",
                "Mechanical Engineering",
            ]
        elif self.LANGUAGE == 'italiano':
            self.ADDRESSES = [
                "Informatica",
                "Elettrotecnica",
                "Meccanica",
            ]

        # Translations set to make the values consistent on the database
        self.TRANSLATIONS = {
            'english_to_italian': {
                'Computer Science': 'Informatica',
                'Electrical Engineering': 'Elettrotecnica',
                'Mechanical Engineering': 'Meccanica',
            },
            'italian_to_english': {
                'Informatica': 'Computer Science',
                'Elettrotecnica': 'Electrical Engineering',
                'Meccanica': 'Mechanical Engineering',
            }
        }

        # Database connection
        self.db = 'school.db'
        self.conn = sqlite3.connect(self.db, check_same_thread=False) # Create a connection object
        self.c = self.conn.cursor() # Create a cursor object to execute SQL queries on the database 

settings = Config() # Get the configuration object modifiable by the user

