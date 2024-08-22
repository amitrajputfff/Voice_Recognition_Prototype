import time
from record import record_audio, extract_features
from authentication import save_features
from store import store_recorded_audio


def setup_profile(user_id):
    features_list = []

    print("Please provide 5 different voice samples. Say different sentences each time.")
    for i in range(5):
        recording_file = f"{user_id}_{i}.wav"
        print(f"Recording sample {i + 1}...")
        record_audio(recording_file)
        print(f"Recording finished and saved as {recording_file}")

        # Wait for a short period to ensure the file system updates
        time.sleep(2)  # Delay for 2 seconds

        # Store recorded audio
        try:
            store_recorded_audio(recording_file)
        except Exception as e:
            print(f"Error during file storage: {e}")
            return

        # Extract features from recorded voice
        features = extract_features(f"stored/{recording_file}")
        if features:
            features_list.append(features)
        else:
            print(f"Error extracting features from {recording_file}.")
            return

    # Save features to database
    if features_list:
        avg_features = {
            'mean': sum(f['mean'] for f in features_list) / len(features_list),
            'std_dev': sum(f['std_dev'] for f in features_list) / len(features_list),
            'max': sum(f['max'] for f in features_list) / len(features_list),
            'min': sum(f['min'] for f in features_list) / len(features_list),
        }
        try:
            save_features(user_id, avg_features)
            print(f"Profile setup completed for user ID {user_id}.")
        except Exception as e:
            print(f"Error saving features: {e}")


if __name__ == "__main__":
    user_id = input("Enter user ID: ")
    setup_profile(user_id)
