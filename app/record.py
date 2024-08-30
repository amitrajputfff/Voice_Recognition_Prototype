import numpy as np
import scipy.io.wavfile as wav
import librosa
import scipy.signal as signal
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


def noise_reduction(data, sr):
    # Apply a high-pass filter to remove low-frequency noise
    sos = signal.butter(10, 100, 'hp', fs=sr, output='sos')
    filtered = signal.sosfilt(sos, data)

    return filtered

def extract_mfcc_features(file_name):
    try:
        data, sr = librosa.load(file_name, sr=None)
        data = noise_reduction(data, sr)

        # Calculate MFCCs
        mfccs = librosa.feature.mfcc(y=data, sr=sr, n_mfcc=13)
        mfcc_mean = np.mean(mfccs, axis=1)
        mfcc_std = np.std(mfccs, axis=1)

        # Convert to Python standard types
        features = {
            'mfcc_mean': mfcc_mean.tolist(),
            'mfcc_std': mfcc_std.tolist()
        }

        return features
    except Exception as e:
        print(f"Error extracting features: {e}")
        return None
