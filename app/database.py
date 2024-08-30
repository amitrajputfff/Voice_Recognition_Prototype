import sqlite3

def connect_db():
    return sqlite3.connect('voice_features.db')  # Replace with your actual database file name

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audio_features (
            user_id TEXT,
            phrase TEXT,
            features BLOB,
            PRIMARY KEY (user_id, phrase)
        )
    ''')
    conn.commit()
    conn.close()

def add_features_column():
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE audio_features ADD COLUMN phrase TEXT")
    except sqlite3.OperationalError as e:
        print(f"Error adding column: {e}")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()
    add_features_column()
