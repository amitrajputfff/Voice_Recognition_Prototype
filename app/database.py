import sqlite3

DATABASE = 'voice_recognition.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audio_features (
            user_id TEXT PRIMARY KEY,
            mean REAL,
            std_dev REAL,
            max REAL,
            min REAL
        )
    ''')
    conn.commit()
    conn.close()

def add_features_column():
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE audio_features ADD COLUMN features TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        print("Column 'features' already exists.")
    conn.close()

if __name__ == "__main__":
    create_table()
    add_features_column()
