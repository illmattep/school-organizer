from flask import Flask, render_template, request, redirect, flash, url_for
import sqlite3
from Text import Text
from config import Config
Text = Text().texts # Get the text dictionary
Config = Config() # Get the configuration object
language = Config.LANGUAGE # Get the language
c = Config.c # Get the cursor object to access the database
conn = Config.conn # Get the connection object to the database

# Create the Flask app
app = Flask(__name__) # Create the Flask app
app.secret_key = 'your secret key' # Set the secret key for the app

# Create the 'classes' table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS classes (
                id INTEGER PRIMARY KEY,
                name TEXT,
                year INTEGER,
                num_students INTEGER,
                creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modification_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                section TEXT,
                address TEXT)''')
conn.commit() # Commit the changes to the database 

# Check if the 'classes' table was created
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='classes'")
if c.fetchone():
    print("The 'classes' table is working.")
else:
    print("Failed to create the 'classes' table.")

# Main page with a form to add a new class
@app.route('/newclass', methods=['GET', 'POST']) # Handle GET and POST requests
def index(): # Function to handle the main page request 
    if request.method == 'POST': # Check if the request method is POST (accessed by submitting the form)
        # Get the form data
        name = request.form['name'] # Class name
        name = name.upper() # Convert the class name to uppercase
        year = int(name[0]) # Year of the class
        section = name[1:].upper() # Section of the class
        num_students = request.form['num_students'] # Number of students
        address = request.form['address'] # Address of the class

        valid = True # Flag to check if the data is valid
        # Check if the data is valid
        if not name or not num_students or not address: # Check if all fields are filled
            valid = False # Data is not valid
            print(Text['fill_required_fields'])
            flash(Text['fill_required_fields'])
            return redirect(url_for('index'))
        if year not in range(1, Config.NUM_YEARS + 1): # Check if the year is valid
            valid = False # Data is not valid
            print(Text['invalid_year'] + ' ' + str(year))
            return redirect(url_for('index'))
        if address not in Config.ADDRESSES: # Check if the address is valid
            valid = False # Data is not valid
            print(Text['invalid_address'])
            flash(Text['invalid_address'])
            return redirect(url_for('index'))

        # Check if the class already exists
        c.execute("SELECT * FROM classes WHERE name = ?", (name,))
        if c.fetchone():
            valid = False
            print(Text['class_exists'])
            flash(Text['class_exists'])
            return redirect(url_for('index'))

        if valid:
            if Config.LANGUAGE == 'italiano': # If the language is Italian, translate the address to English, to avoid inconsistencies in the database
                address = Config.TRANSLATIONS['italian_to_english'].get(address, address)
            c.execute("INSERT INTO classes (name, year, num_students, address, section) VALUES (?, ?, ?, ?, ?)", (name, year, num_students, address, section))
            conn.commit()
            print(Text['class_added' + ': ' + name + ', ' + str(year) + ', ' + section + ', ' + num_students + ', ' + address])
            return redirect('/')
    else: # If the request method is GET (accessed by visiting the page without submitting the form)
        # Get all classes from the database
        c.execute("SELECT * FROM classes") # Execute an SQL query to select all rows from the 'classes' table
        classes = c.fetchall() # Fetch all rows from the result of the query
        return render_template('addnewclass.html', classes=classes, addresses=Config.ADDRESSES, language=language, Text=Text) # Render the 'index.html' template with the classes, addresses, language, and Text object

if __name__ == '__main__':
    app.run(debug=True)
