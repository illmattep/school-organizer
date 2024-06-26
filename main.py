from flask import Flask, render_template, request, redirect, url_for
from Text import TextClassobj
from config import settings
from POSTHANDLER import PostHandler
from flask_sqlalchemy import SQLAlchemy # Import the SQLAlchemy class from the flask_sqlalchemy module to work with the database
from flask_paginate import Pagination, get_page_parameter
from utils import Utils
from subjects import SubjectManagerobj
from teachers import TeacherManagerobj
from classes import ClassManagerobj

 # Get the text dictionary
language = settings.LANGUAGE # Get the language
c = settings.c # Get the cursor object to access the database
conn = settings.conn # Get the connection object to the database
PostHandler = PostHandler() # Create the PostHandler object
utils = Utils() # Create the utils object

# Create the Flask app
app = Flask(__name__) # Create the Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///settings.db' # Set the URI for the database
db = SQLAlchemy(app)
app.secret_key = 'b3dsm0v3rs' # Set the secret key for the app

# Inject the Text object into the context of the app
@app.context_processor
def inject_text():
    return dict(Text=TextClassobj.texts)

# newclass page with a form to add a new class
@app.route('/newclass', methods=['GET', 'POST']) # Handle GET and POST requests
def newclass(): # Function to handle the main page request 
    if request.method == 'POST': # Check if the request method is POST (accessed by submitting the form)
        return PostHandler.newclass_posthandler()
    else: # If the request method is GET (accessed by visiting the page without submitting the form)
        # Get all classes from the database
        c.execute("SELECT * FROM classes") # Execute an SQL query to select all rows from the 'classes' table
        classes = c.fetchall() # Fetch all rows from the result of the query    
        return render_template('pages/addnewclass.html', classes=classes, addresses=settings.ADDRESSES, language=language) # Render the 'index.html' template with the classes, addresses, language, and Text object

# delete class page with a form to delete a class
@app.route('/deleteclass/<int:id>', methods=['POST'])
def deleteclass(id):
    ClassManagerobj.delete_class(id) # Delete the class with the specified ID
    # Redirect back to the class list
    return redirect(url_for('classlist'))

# classlist table page with a list of classes in a table
@app.route('/viewclasses', methods=['GET', 'POST']) # Handle GET requests
def classlist():
    if request.method == 'POST':
        pass
    else:
        search = request.args.get('search', '')
        sort = request.args.get('sort', 'name')
        page = request.args.get(get_page_parameter(), type=int, default=1)
        per_page = request.args.get('per_page', type=int, default=10)

        # Calculate offset for pagination
        offset = (page - 1) * per_page

        # Use raw SQL for search and sort
        query = f"SELECT * FROM classes WHERE name LIKE ? ORDER BY {sort} LIMIT ? OFFSET ?"
        params = ('%' + search + '%', per_page, offset)
        c.execute(query, params)
        classes = c.fetchall()

        # Get total number of classes for pagination
        c.execute("SELECT COUNT(*) FROM classes WHERE name LIKE ?", ('%' + search + '%',))
        total = c.fetchone()[0]

        pagination = Pagination(page=page, total=total, per_page=per_page, search=search, record_name='classes')
        pagination_links = utils.get_pagination_links(page, pagination.total_pages)

        return render_template('pages/viewclasses.html', classes=classes, addresses=settings.ADDRESSES, language=language, pagination=pagination, pagination_links=pagination_links) 

# edit class page with a form to edit a class
@app.route('/editclass/<int:id>', methods=['GET', 'POST'])
def editclass(id):
    if request.method == 'POST':
        if request.form.get('form_identifier') == 'editclassfromlist':
            c.execute("SELECT * FROM classes WHERE id = ?", (id,))
            class_data = c.fetchone()
            return render_template('pages/editclass.html', class_data=class_data, addresses=settings.ADDRESSES, language=language)
    else:
        c.execute("SELECT * FROM classes WHERE id = ?", (id,))
        class_data = c.fetchone()
        return render_template('pages/editclass.html', class_data=class_data, addresses=settings.ADDRESSES, language=language)

# settings page
@app.route('/settings', methods=['GET', 'POST'])
def settingspage():
    if request.method == 'POST':
        PostHandler.settings_posthandler()
        return redirect(url_for('settingspage'))
    else:
        if settings.DEBUG:
            print("Loaded languages: " + str(list(TextClassobj.check_language(settings.LANGUAGES_PATH)))) # Convert dict_keys to a list and then to a string
        return render_template('pages/settings.html', addresses=settings.ADDRESSES, language=language, installed_languages=list(TextClassobj.check_language(settings.LANGUAGES_PATH)), settings=settings, all_languages=TextClassobj.allpossiblelanguages) # Convert dict_keys to a list
    
# home page with a dashboard of functionalities
@app.route('/', methods=['GET', 'POST']) # Handle GET requests
@app.route('/home', methods=['GET', 'POST']) # Handle GET requests
@app.route('/index', methods=['GET', 'POST']) # Handle GET requests
def home():
    if request.method == 'POST': # Check if the request method is POST (accessed by submitting the form)
        # check if the submit button is the one for adding a new class by checking the hidden input field value of the form, if hidden input is not there do nothing
        if request.form.get('form_identifier') == 'addnewclass':
            print('SUBMIT BUTTON CLICKED FROM: ' + request.url + ' with request: ' + request.form.get('form_identifier'))
            return PostHandler.newclass_posthandler()
    # Get all classes from the database
    c.execute("SELECT * FROM classes")
    classes = c.fetchall()
    return render_template('pages/home.html', classes=classes, addresses=settings.ADDRESSES, language=language)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
