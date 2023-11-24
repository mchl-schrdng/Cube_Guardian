import sqlite3
import os

def init_db():
    # Get the directory of the current script
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # Construct the path to the database file
    db_path = os.path.join(dir_path, 'tables', 'cube_test_results.db')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables if they do not exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS overall_status (
            id INTEGER PRIMARY KEY,
            date TEXT,
            status TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cube_status (
            id INTEGER PRIMARY KEY,
            date TEXT,
            cube_name TEXT,
            status TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dimension_status (
            id INTEGER PRIMARY KEY,
            date TEXT,
            cube_name TEXT,
            dimension TEXT,
            status TEXT,
            error_message TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_test_result(table_name, data):
    # Get the directory of the current script
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # Construct the path to the database file
    db_path = os.path.join(dir_path, 'tables', 'cube_test_results.db')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    if table_name == 'overall_status':
        cursor.execute('INSERT INTO overall_status (date, status) VALUES (?, ?)', data)
    elif table_name == 'cube_status':
        cursor.execute('INSERT INTO cube_status (date, cube_name, status) VALUES (?, ?, ?)', data)
    elif table_name == 'dimension_status':
        cursor.execute('INSERT INTO dimension_status (date, cube_name, dimension, status, error_message) VALUES (?, ?, ?, ?, ?)', data)
    conn.commit()
    conn.close()

# Initialize the database when the script is run
if __name__ == "__main__":
    init_db()