from flask import Flask, render_template, request, redirect, flash, url_for
import sqlite3
from Text import Text
from config import Config

Text = Text().texts # Get the text dictionary
Config = Config() # Get the configuration object
language = Config.LANGUAGE # Get the language
c = Config.c # Get the cursor object to access the database
conn = Config.conn # Get the connection object to the database

class PostHandler:
    def newclass_posthandler(self):
        # Get the form data
        name = request.form['name'] # Class name
        name = name.upper() # Convert the class name to uppercase
        try:
            year = int(name[0]) # Check if the first character of the class name is a number
        except ValueError: # If the first character is not a number
            print(Text['invalid_year'])
            flash(Text['invalid_year'], 'error')
            return redirect(url_for('newclass'))
        section = name[1:].upper() # Section of the class
        num_students = request.form['num_students'] # Number of students
        address = request.form['address'] # Address of the class

        print(name, year, section, num_students, address)
        valid = True # Flag to check if the data is valid
        # Check if the data is valid
        if not name or not num_students or not address: # Check if all fields are filled
            valid = False # Data is not valid
            print(Text['fill_required_fields'])
            flash(Text['fill_required_fields'], 'error')
            return redirect(url_for('newclass'))
        if year not in range(1, Config.NUM_YEARS + 1): # Check if the year is valid
            valid = False # Data is not valid
            print(Text['invalid_year'] + ' ' + str(year))
            flash(Text['invalid_year'], 'error')
            return redirect(url_for('newclass'))
        if address not in Config.ADDRESSES: # Check if the address is valid
            valid = False # Data is not valid
            print(Text['invalid_address'])
            flash(Text['invalid_address'], 'error')
            return redirect(url_for('newclass'))

        # Check if the class already exists
        c.execute("SELECT * FROM classes WHERE name = ?", (name,))
        if c.fetchone():
            valid = False
            print(Text['class_exists'])
            flash(Text['class_exists'], 'error')
            return redirect(url_for('newclass'))

        if valid:
            if Config.LANGUAGE == 'italiano': # If the language is Italian, translate the address to English, to avoid inconsistencies in the database
                address = Config.TRANSLATIONS['italian_to_english'].get(address, address)
            c.execute("INSERT INTO classes (name, year, num_students, address, section) VALUES (?, ?, ?, ?, ?)", (name, year, num_students, address, section))
            conn.commit()
            flash(Text['class_added'], 'success')
            print(Text['class_added'] + ': ' + name + ', ' + str(year) + ', ' + section + ', ' + num_students + ', ' + address)
            return redirect(url_for('newclass'))