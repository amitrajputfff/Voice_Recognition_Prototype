import json
import numpy as np
from database import connect_db

def save_features(features_list):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        for features in features_list:
            user_id = features['user_id']
            phrase = features['phrase']
            feature_data = json.dumps({
                'mfcc_mean': features['mfcc_mean'],
                'mfcc_std': features['mfcc_std']
            })
            cursor.execute('''
                INSERT OR REPLACE INTO audio_features (user_id, phrase, features)
                VALUES (?, ?, ?)
            ''', (user_id, phrase, feature_data))
        conn.commit()
        conn.close()
        print(f"Saved features for all samples.")
    except Exception as e:
        print(f"Error saving features: {e}")

def get_stored_features(user_id, phrase):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT features FROM audio_features WHERE user_id = ? AND phrase = ?', (user_id, phrase))
        result = cursor.fetchone()
        conn.close()
        if result:
            features = json.loads(result[0])

            return features
        return None
    except Exception as e:
        print(f"Error fetching stored features: {e}")
        return None

def authenticate(features, stored_features, tolerance=10.0):
    diffs = []
    for i in range(len(features['mfcc_mean'])):
        mean_diff = abs(features['mfcc_mean'][i] - stored_features['mfcc_mean'][i])
        std_diff = abs(features['mfcc_std'][i] - stored_features['mfcc_std'][i])
        diffs.append(mean_diff + std_diff)

    mean_diff = np.mean(diffs)
    print(f"Feature differences: {mean_diff}")
    return mean_diff < tolerance
