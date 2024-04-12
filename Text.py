from config import Config

Config = Config()
language = Config.LANGUAGE

class Text:
    def __init__(self):
        self.english = {
            'class_line': ['Year', 'Section', 'Number of Students', 'Creation Date', 'Modification Date', 'Address'], # may be deprecated
            'page_titles': {
                'home': 'Home',
                'classes': 'Classes',
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
            'class_name_info': "or example: input ''3EIN'' will take 3 as the year and EIN as the section",
            'num_students_label': "Number of Students:",
            'address_label': "Address:",
            'submit_button_text': "Add",
            # Add more text lines as needed
        }

        self.italiano = {
            'class_line': ['Anno', 'Sezione', 'Numero Studenti', 'Data di Creazione', 'Data di Modifica', 'Indirizzo'], # may be deprecated
            'page_titles': {
                'home': 'Home',
                'classes': 'Classi',
                'teachers': 'Insegnanti',
                'students': 'Studenti',
            },
            'page_title': 'Sistema di Gestione Scolastica',
            'welcome_message': 'Benvenuto nel nostro sistema di gestione scolastica!',
            'class_added': 'Classe aggiunta con successo!',
            'class_exists': 'La classe esiste già!',
            'invalid_year': 'Anno non valido!',
            'invalid_address': 'Indirizzo non valido!',
            'fill_required_fields': 'Si prega di compilare tutti i campi obbligatori!',
            'class_deleted': 'Classe eliminata con successo!',
            'webpage_title': "Sistema Gestionale Scuola",
            'classes_heading': "Classi",
            'year_label': "Anno:",
            'num_students_label': "Numero Studenti:",
            'address_label': "Indirizzo",
            'section_label': "Sezione",
            'add_new_class_heading': "Aggiungi Nuova Classe",
            'class_name_label': "Nome Classe:",
            'class_name_info': "esempio: input ''3EIN'' prenderà 3 come anno e EIN come sezione",
            'num_students_label': "Numero Studenti:",
            'address_label': "Indirizzo:",
            'submit_button_text': "Aggiungi",
            # Aggiungi altre righe di testo se necessario
        }
        self.texts = self.valueof(language)
    def get_text(self, key):
        return self.texts.get(key, '')

    def set_text(self, key, value):
        self.texts[key] = value

    def valueof(self, language):
        return self.english if language == 'english' else self.italiano