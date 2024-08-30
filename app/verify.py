import time
import random
from record import record_audio, extract_mfcc_features
from phrases import phrases
from authentication import get_stored_features, authenticate


def verify_voice(user_id):
    # Select a phrase for the user to say
    phrase_to_verify = random.choice(phrases)

    print(f"Please say the following phrase: '{phrase_to_verify}'")
    time.sleep(2)  # Short delay to give user time to prepare

    # Record the user's voice
    recording_file = "verify_temp.wav"
    record_audio(recording_file)  # Adjust duration as needed

    # Extract features from the recorded voice
    features = extract_mfcc_features(recording_file)
    if features is None:
        print("Error extracting features from the recorded audio.")
        return

    # Retrieve stored features for the specific user and phrase
    stored_features = get_stored_features(user_id, phrase_to_verify)
    if stored_features is None:
        print(f"No stored features found for user ID {user_id} and phrase '{phrase_to_verify}'.")
        return

    # Authenticate the user by comparing features
    is_authenticated = authenticate(features, stored_features, tolerance=10.0)  # Adjust tolerance as needed

    if is_authenticated:
        print(f"Voice verification successful for user ID {user_id}.")
    else:
        print(f"Voice verification failed for user ID {user_id}.")


if __name__ == "__main__":
    user_id = input("Enter user ID: ")
    verify_voice(user_id)
