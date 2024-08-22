import sqlite3

def initialize_database():
    conn = sqlite3.connect('voice_recognition.db')
    cursor = conn.cursor()

    # Create the audio_features table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS audio_features (
        user_id TEXT PRIMARY KEY,
        mean REAL,
        std_dev REAL,
        max REAL,
        min REAL
    )
    ''')

    # Commit and close the connection
    conn.commit()
    conn.close()
    print("Database initialized.")

if __name__ == "__main__":
    initialize_database()
