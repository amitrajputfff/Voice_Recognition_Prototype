import sqlite3
import json
import numpy as np
from database import connect_db


def save_features(user_id, features):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO audio_features (user_id, mean, std_dev, max, min)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, features['mean'], features['std_dev'], features['max'], features['min']))
    conn.commit()
    conn.close()


def get_stored_features(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT mean, std_dev, max, min FROM audio_features WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            'mean': row[0],
            'std_dev': row[1],
            'max': row[2],
            'min': row[3]
        }
    return None


def authenticate(features, stored_features):
    # Calculate differences between features
    max_diff = abs(features['max'] - stored_features['max'])
    mean_diff = abs(features['mean'] - stored_features['mean'])
    std_dev_diff = abs(features['std_dev'] - stored_features['std_dev'])
    min_diff = abs(features['min'] - stored_features['min'])

    # Print the differences for debugging
    print(
        f"Feature differences: mean_diff={mean_diff}, std_dev_diff={std_dev_diff}, max_diff={max_diff}, min_diff={min_diff}")

    # Tolerance levels (adjusted based on observed differences)
    tolerance = {
        'mean': 0.2,  # Allowable difference in mean
        'std_dev': 100,  # Allowable difference in standard deviation
        'max': 300,  # Allowable difference in max value
        'min': 300  # Allowable difference in min value
    }

    return (mean_diff < tolerance['mean'] and
            std_dev_diff < tolerance['std_dev'] and
            max_diff < tolerance['max'] and
            min_diff < tolerance['min'])
