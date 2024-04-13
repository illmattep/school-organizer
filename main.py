from flask import Flask, render_template, request, redirect, flash, url_for
import sqlite3
from Text import Text
from config import Config
from POSTHANDLER import PostHandler

Text = Text().texts # Get the text dictionary
Config = Config() # Get the configuration object
language = Config.LANGUAGE # Get the language
c = Config.c # Get the cursor object to access the database
conn = Config.conn # Get the connection object to the database
PostHandler = PostHandler() # Create the PostHandler object

# Create the Flask app
app = Flask(__name__) # Create the Flask app
app.secret_key = 'b3dsm0v3rs' # Set the secret key for the app
# Create the 'classes' table in the database
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

@app.context_processor
def inject_text():
    return dict(Text=Text)

# newclass page with a form to add a new class
@app.route('/newclass', methods=['GET', 'POST']) # Handle GET and POST requests
def newclass(): # Function to handle the main page request 
    if request.method == 'POST': # Check if the request method is POST (accessed by submitting the form)
        # check if the submit button is the one for adding a new class by checking the hidden input field value of the form
        if request.form.get('form_identifier') == 'addnewclass':
            return PostHandler.newclass_posthandler()
    else: # If the request method is GET (accessed by visiting the page without submitting the form)
        # Get all classes from the database
        print('SUBMIT BUTTON CLICKED FROM: ' + request.url)
        c.execute("SELECT * FROM classes") # Execute an SQL query to select all rows from the 'classes' table
        classes = c.fetchall() # Fetch all rows from the result of the query    
        return render_template('pages/addnewclass.html', classes=classes, addresses=Config.ADDRESSES, language=language, Text=Text) # Render the 'index.html' template with the classes, addresses, language, and Text object

# home page with a list of classes
@app.route('/', methods=['GET', 'POST']) # Handle GET requests
@app.route('/home', methods=['GET', 'POST']) # Handle GET requests
@app.route('/index', methods=['GET', 'POST']) # Handle GET requests
def home():
    if request.method == 'POST': # Check if the request method is POST (accessed by submitting the form)
        # check if the submit button is the one for adding a new class by checking the hidden input field value of the form
        if request.form.get('form_identifier') == 'addnewclass':
            return PostHandler.newclass_posthandler()
    # Get all classes from the database
    c.execute("SELECT * FROM classes")
    classes = c.fetchall()
    return render_template('pages/home.html', classes=classes, addresses=Config.ADDRESSES, language=language, Text=Text)


if __name__ == '__main__':
    app.run(debug=True)
