import sqlite3

DATABASE = 'voice_recognition.db'


def setup_database():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Create table if it does not exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audio_features (
                user_id TEXT PRIMARY KEY,
                features TEXT
            )
        ''')

        # Commit changes and close connection
        conn.commit()
        conn.close()
        print("Database setup complete.")
    except Exception as e:
        print(f"Error setting up database: {e}")


if __name__ == "__main__":
    setup_database()
