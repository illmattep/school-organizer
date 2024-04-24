from config import settings

class classesmanager:
    def __init__(self) -> None:
        self.language = settings.LANGUAGE
        self.c = settings.c
        self.conn = settings.conn

        # Create the 'classes' table in the database
        self.c.execute('''CREATE TABLE IF NOT EXISTS classes (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        year INTEGER,
                        num_students INTEGER,
                        creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        modification_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        section TEXT,
                        address TEXT)''')
        self.conn.commit() # Commit the changes to the database 

        # Check if the 'classes' table was created
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='classes'")
        if self.c.fetchone():
            print("The 'classes' table is working.")
        else:
            print("Failed to create the 'classes' table.")

    
    def delete_class(self, id):
        self.c.execute("DELETE FROM classes WHERE id = ?", (id,))
        self.conn.commit()
        if settings.DEBUG:
            print(f"Deleted class with id {id}")    

    def add_class(self, name, year, num_students, address, section):
        self.c.execute("INSERT INTO classes (name, year, num_students, address, section) VALUES (?, ?, ?, ?, ?)", (name, year, num_students, address, section))
        self.conn.commit()
        if settings.DEBUG:
            print(f"Added class with values: {name}, {year}, {num_students}, {address}, {section}")



ClassManagerobj = classesmanager()