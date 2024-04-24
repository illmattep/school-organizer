from flask import Flask, render_template, request, redirect, flash, url_for
import sqlite3
from Text import TextClassobj
from teachers import TeacherManagerobj
from subjects import SubjectManagerobj
from classes import ClassManagerobj
from config import settings
import time
import threading

TextClassobj # Get the text dictionary
language = settings.LANGUAGE # Get the language
c = settings.c # Get the cursor object to access the database
conn = settings.conn # Get the connection object to the database

class PostHandler:
    def newclass_posthandler(self):
        print('newclass posthandler has been called by: ' + request.url)
        # Get the form data
        name = request.form['name'] # Class name
        name = name.upper() # Convert the class name to uppercase
        try:
            year = int(name[0]) # Check if the first character of the class name is a number
        except ValueError: # If the first character is not a number
            print(TextClassobj.texts['invalid_year'])
            flash(TextClassobj.texts['invalid_year'], 'error')
            return redirect(url_for('newclass'))
        section = name[1:].upper() # Section of the class
        num_students = request.form['num_students'] # Number of students
        address = request.form['address'] # Address of the class

        print("trying to add a class with values: ", name, year, section, num_students, address)
        valid = True # Flag to check if the data is valid
        # Check if the data is valid
        if not name or not num_students or not address: # Check if all fields are filled
            valid = False # Data is not valid
            print(TextClassobj.texts['fill_required_fields'])
            flash(TextClassobj.texts['fill_required_fields'], 'error')
            return redirect(url_for('newclass'))
        if year not in range(1, settings.NUM_YEARS + 1): # Check if the year is valid
            valid = False # Data is not valid
            print(TextClassobj.texts['invalid_year'] + ' ' + str(year))
            flash(TextClassobj.texts['invalid_year'], 'error')
            return redirect(url_for('newclass'))
        if address not in settings.ADDRESSES: # Check if the address is valid
            valid = False # Data is not valid
            print(TextClassobj.texts['invalid_address'])
            flash(TextClassobj.texts['invalid_address'], 'error')
            return redirect(url_for('newclass'))

        # Check if the class already exists
        c.execute("SELECT * FROM classes WHERE name = ?", (name,))
        if c.fetchone():
            valid = False
            print(TextClassobj.texts['class_exists'])
            flash(TextClassobj.texts['class_exists'], 'error')
            return redirect(url_for('newclass'))

        if valid:
            if settings.LANGUAGE == 'italiano': # If the language is Italian, translate the address to English, to avoid inconsistencies in the database
                address = settings.TRANSLATIONS['italian_to_english'].get(address, address)
            ClassManagerobj.add_class(name, year, num_students, address, section) # Add the class to the database
            flash(TextClassobj.texts['class_added'], 'success')
            print(TextClassobj.texts['class_added'] + ': ' + name + ', ' + str(year) + ', ' + section + ', ' + num_students + ', ' + address)
            return redirect(url_for('newclass'))
        


    # ! SETTINGS STUFF AHEAD
    def settings_posthandler(self):
        if request.form.get('form_identifier') == 'language_tab':
            # check if the button pressed to submit the form has a certain value
            if request.form.get('submit') == 'translation_install':
                if settings.DEBUG:
                    print('SUBMIT BUTTON CLICKED FROM: ' + request.url + ' with request: ' + request.form.get('form_identifier'))
                    print('Language to translate: ' + request.form.get('language_to_translate'))
                language_to_translate = request.form.get('language_to_translate')
                flash(f"Installing translation for {language_to_translate}...", 'warning')
                threading.Thread(target=self.translation_install, args=(language_to_translate,)).start()
                return redirect(url_for('settingspage'))
            elif request.form.get('submit') == 'change_language':
                if settings.DEBUG:
                    print('SUBMIT BUTTON CLICKED FROM: ' + request.url + ' with request: ' + request.form.get('form_identifier'))
                    print('Trying to change language')
                TextClassobj.change_language(request.form.get('language'))
                print('Language changed to: ' + request.form.get('language'))
                print()
        elif request.form.get('form_identifier') == 'database_tab':
            if settings.DEBUG:
                print('SUBMIT BUTTON CLICKED FROM: ' + request.url + ' with request: ' + request.form.get('form_identifier'))
                print('Trying to change database settings')
            return PostHandler.database_settings() # TODO: Implement database settings post handler
        elif request.form.get('form_identifier') == 'backup_tab':
            if settings.DEBUG:
                print('SUBMIT BUTTON CLICKED FROM: ' + request.url + ' with request: ' + request.form.get('form_identifier'))
                print('Trying change backup settings')
            return PostHandler.backup_database() # TODO: Implement database backup post handler

    def translation_install(self, language_to_translate):
        TextClassobj.translate_to_json(language_to_translate)
    