import time
from record import record_audio, extract_features
from authentication import get_stored_features, authenticate
from store import store_recorded_audio

def verify_voice(user_id):
    # Record new voice sample
    recording_file = f"{user_id}.wav"
    print("Recording audio...")
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
    if not features:
        print(f"Error extracting features from {recording_file}.")
        return

    # Retrieve stored features
    stored_features = get_stored_features(user_id)
    if not stored_features:
        print(f"No features found for user ID {user_id}.")
        return

    # Authenticate voice
    if authenticate(features, stored_features):
        print("Voice authenticated successfully!")
    else:
        print("Voice authentication failed.")

if __name__ == "__main__":
    user_id = input("Enter user ID: ")
    verify_voice(user_id)
