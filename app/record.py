import numpy as np
import scipy.io.wavfile as wav
import sounddevice as sd


def record_audio(file_name):
    try:
        fs = 44100  # Sample rate
        duration = 3  # Duration in seconds
        print("Recording...")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()  # Wait until recording is finished
        wav.write(file_name, fs, recording)
        print(f"Recording finished and saved as {file_name}")
    except Exception as e:
        print(f"Error recording audio: {e}")


def extract_features(file_name):
    try:
        fs, data = wav.read(file_name)
        if data.ndim > 1:
            data = np.mean(data, axis=1)  # Convert to mono if stereo

        # Convert to Python standard types
        features = {
            'mean': float(np.mean(data)),
            'std_dev': float(np.std(data)),
            'max': float(np.max(data)),
            'min': float(np.min(data))
        }

        print(f"Extracted features from {file_name}: {features}")
        return features
    except Exception as e:
        print(f"Error extracting features: {e}")
        return None
