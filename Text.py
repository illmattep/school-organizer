from config import settings
import os
import json
from config import settings
from translate import Translator

language = settings.LANGUAGE

class Text:
    english = {
        'class_line': ['Year', 'Section', 'Number of Students', 'Creation Date', 'Modification Date', 'Address'], # may be deprecated
        'page_titles': {
            'home': 'Home',
            'classes': 'Classes',
            'classes_list': 'Classes List',
            'teachers': 'Teachers',
            'students': 'Students',
        },
        'welcome_message': 'Welcome to our school management system!',
        'class_added': 'Class added successfully!',
        'class_exists': 'Class already exists!',
        'invalid_year': 'Invalid year!',
        'invalid_address': 'Invalid address!',
        'fill_required_fields': 'Please fill in all required fields!',
        'class_deleted': 'Class deleted successfully!',
        'webpage_title': "School Management System",
        'classes_heading': "Classes",
        'year_label': "Year:",
        'num_students_label': "Number of Students:",
        'address_label': "Address:",
        'section_label': "Section:",
        'add_new_class_heading': "Add New Class",
        'class_name_label': "Class Name:",
        'class_name_info': "or example: input 3EIN will take 3 as the year and EIN as the section",
        'num_students_label': "Number of Students:",
        'address_label': "Address:",
        'submit_button_text': "Add",
        'class_table': {
            'filters': {
                'search_placeholder': 'Search...',
                'search_button': 'Search',
            },
            'id': 'ID',
            'name': 'Name',
            'year': 'Year',
            'num_students': 'Number of Students',
            'creation_date': 'Creation Date',
            'modification_date': 'Modification Date',
            'section': 'Section',
            'address': 'Address',
        },
        'sidebar': {
            'home': 'Home',
            'newclass': 'Add Class',
            'classlist': 'Class List',
            'teachers': 'Teachers',
            'settings': 'Settings',
        },
        'settings': {
            'tabs': {
                'language': 'Language',
                'database': 'Database',
                'backup': 'Backup',
            },
            'language_tab': {
                'selected_language': 'Selected Language',
                'install_language': 'Install Language',
                'install_translation_button': 'Install translation',
            },
            'database_tab': {
                'path_database': 'Path to local database file',
            },
            'backup_tab': {
                'path_backup': 'Path to backups'
            },
            'submit_button_save_changes': 'Save changes',
        },
        # Add more text lines as needed
    }

    # TODO: Write the english language to json automatically 

    
    def __init__(self):
        print("Text class initialized")
        self.allpossiblelanguages = {
            "arabic": "ar",
            "deutch": "de",
            "english": "en",
            "spanish": "es",
            "french": "fr",
            "hebrew": "he",
            "italian": "it",
            "dutch": "nl",
            "polish": "pl",
            "portuguese": "pt",
            "russian": "ru",
            "turkish": "tr",
            "chinese": "zh",
        }
        # check if languagepath/english.json exists
        if not os.path.exists(settings.LANGUAGES_PATH + "/english.json"):
            if not os.path.exists(settings.LANGUAGES_PATH):
                if settings.DEBUG:
                    print("Languages folder does not exist. Creating one and installing english.json...")
                os.makedirs(settings.LANGUAGES_PATH)
                self.translate_to_json("english")
            else:
                if settings.DEBUG:
                    print("Languages folder exists but english language is missing. Installing english.json...")
                self.translate_to_json("english")

        self.languages = self.check_language(settings.LANGUAGES_PATH)
        self.texts = self.valueof(language)

    @staticmethod
    def check_language(folder_path):
        languages = {}
        for filename in os.listdir(folder_path):
            if filename.endswith('.json'):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    if all(voice in data for voice in Text.english.keys()):
                        language = os.path.splitext(filename)[0]
                        languages[language] = data
        return languages


    def translate_to_json(self, to_language, from_language="en", text=english):
        language_name = to_language
        to_language = self.allpossiblelanguages.get(to_language)
        translator = Translator(to_lang=to_language, from_lang=from_language, secret_access_key=None, debug=settings.DEBUG)
        translated_dict = {}

        def translate_recursive(data):
            translated_data = {}                                                                                                    
            for key, value in data.items():
                if isinstance(value, dict):
                    if settings.DEBUG:
                        print(f"Translating {key}...")                                                                                                      
                    translated_value = translate_recursive(value)
                    if settings.DEBUG:
                        print(f"Translated {key} to {translated_value}")
                elif isinstance(value, list):
                    if settings.DEBUG:
                        print(f"Translating {key}...")
                    translated_value = ' '.join([translator.translate(v) for v in value])
                    if settings.DEBUG:
                        print(f"Translated {key} to {translated_value}")
                else:
                    try:
                        if settings.DEBUG:
                            print(f"Translating {key}...")
                        translated_value = translator.translate(value)
                        if settings.DEBUG:
                            print(f"Translated {key} to {translated_value}")
                    except StopIteration:
                        if settings.DEBUG:
                            print(f"Failed to translate {key}")
                        translated_value = None
                translated_data[key] = translated_value
            return translated_data

        translated_dict = translate_recursive(text)

        # parse to json and save as "to_language".json
        file_path = os.path.join(settings.LANGUAGES_PATH, f"{language_name}.json")
        with open(file_path, 'w') as file:
            json.dump(translated_dict, file)

    def get_text(self, key): # * UNUSED
        return self.texts.get(key, '')

    def set_text(self, key, value): # * UNUSED
        self.texts[key] = value

    def valueof(self, language):
        return self.english if language == 'english' else self.italiano
    
    def change_language(self, language):
        print(f"Changing language to {language}")
        chosen_language = language.lower()
        print(f"Chosen language: {chosen_language}")
        file_path = os.path.join(settings.LANGUAGES_PATH, f"{chosen_language}.json")
        print(f"File path: {file_path}")
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
                if all(voice in data for voice in Text.english.keys()):
                    print(f"Successfully changed language to {chosen_language}")
                    self.texts = data
                    print(self.texts)
                else:
                    print(f"The {chosen_language}.json file does not contain all the required keys.")
        else:
            print(f"The {chosen_language}.json file does not exist.")

TextClassobj = Text()