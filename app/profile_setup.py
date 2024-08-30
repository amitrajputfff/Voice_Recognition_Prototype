import time
from record import extract_mfcc_features, record_audio
from authentication import save_features
from store import store_recorded_audio
from fuzzywuzzy import fuzz
import speech_recognition as sr
from phrases import phrases  # Import the list of phrases


def record_with_phrase_detection(file_name, phrase_to_recognize):
    recognizer = sr.Recognizer()

    print(f"Please say the following phrase: '{phrase_to_recognize}'")
    time.sleep(2)

    # Record the audio
    record_audio(file_name)

    # Recognize the speech using Google Web Speech API
    with sr.AudioFile(file_name) as source:
        audio = recognizer.record(source)
        print("Processing...")

    try:
        recognized_text = recognizer.recognize_google(audio)
        print(f"Recognized text: '{recognized_text}'")

        # Normalize text to lowercase and remove whitespace for comparison
        normalized_recognized_text = recognized_text.lower().strip()
        normalized_phrase_to_recognize = phrase_to_recognize.lower().strip()

        # Use fuzzy matching to allow for minor differences
        similarity_score = fuzz.ratio(normalized_recognized_text, normalized_phrase_to_recognize)
        print(f"Similarity score: {similarity_score}")

        if similarity_score > 80:  # Adjust the threshold as needed
            return True
        else:
            print("Phrase did not match.")
            return False

    except sr.UnknownValueError:
        print("Sorry, could not understand the audio.")
        return False
    except sr.RequestError as e:
        print(f"Sorry, there was an error with the request: {e}")
        return False


def profile_setup(user_id):
    features_list = []

    # Use the list of phrases directly
    if len(phrases) < 5:
        print("Not enough phrases available. Please add more phrases.")
        return

    for i, phrase in enumerate(phrases[:5]):  # Select the first 5 phrases
        recording_file = f"{user_id}_{i}.wav"

        # Retry loop for recording a valid phrase
        while True:
            print(f"Recording sample {i + 1}...")
            if record_with_phrase_detection(recording_file, phrase):
                break
            else:
                print(f"Failed to recognize the phrase for sample {i + 1}. Please try again.")

        # Store recorded audio
        try:
            store_recorded_audio(recording_file)
        except Exception as e:
            print(f"Error during file storage: {e}")
            return

        # Extract features from recorded voice
        features = extract_mfcc_features(f"stored/{recording_file}")
        if features:
            features['phrase'] = phrase  # Add phrase to features
            features['user_id'] = user_id  # Add user ID to features
            features_list.append(features)
        else:
            print(f"Error extracting features from {recording_file}.")
            return

    # Save features to database
    if features_list:
        try:
            save_features(features_list)  # Save all features
            print(f"Profile setup completed for user ID {user_id}.")
        except Exception as e:
            print(f"Error saving features: {e}")


if __name__ == "__main__":
    user_id = input("Enter user ID: ")
    profile_setup(user_id)
