import sqlite3

def init_db():
    conn = sqlite3.connect('services/db/tables/schedule.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY,
            schedule_type TEXT,
            schedule_time TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_schedule(schedule_type, schedule_time):
    conn = sqlite3.connect('db/tables/schedule.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO schedules (schedule_type, schedule_time) VALUES (?, ?)', (schedule_type, schedule_time))
    conn.commit()
    conn.close()

def get_all_schedules():
    conn = sqlite3.connect('db/tables/schedule.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, schedule_type, schedule_time FROM schedules')
    schedules = cursor.fetchall()
    conn.close()
    return schedules

def delete_schedule(schedule_id):
    conn = sqlite3.connect('db/tables/schedule.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM schedules WHERE id = ?', (schedule_id,))
    conn.commit()
    conn.close()