# pip install SpeechRecognition
# brew install portaudio
# pip install pyaudio

import time
import pyaudio
import numpy as np
import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Threshold for starting/stopping speech recognition (energy level)
DURATION = 0.05  # Record for 0.1 seconds
RATE = 44100    # Sample rate (44.1 kHz is typical for audio)
CHUNK = int(RATE * DURATION)  # Number of samples for 0.1 seconds
THRESHOLD = 10000  # This value is arbitrary; adjust based on your environment
SILENCE_TIMEOUT = 3  # Time in seconds to wait for silence before stopping

def start_listening():
    # Initialize PyAudio
    p = pyaudio.PyAudio()
    
    # Open audio stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    try:
        print("Starting audio capture...")
        while True:
            time.sleep(0.01)
            # Read a 0.1-second chunk of audio data
            data = stream.read(CHUNK, exception_on_overflow=False)
            
            # Calculate the peak energy of the audio chunk
            peak = calculate_peak(data)
            print(f"Peak value: {peak}")
            
            # Check if the peak exceeds the threshold
            if peak > THRESHOLD:
                print("Speech detected!")
                # Initialize recognizer
                recognizer = sr.Recognizer()
                
                # Access microphone
                with sr.Microphone() as source:
                    speech_content = capture_speech(recognizer, source)  # Start speech recognition
                    return speech_content

    except KeyboardInterrupt:
        print("Audio capture stopped.")

    finally:
        # Close the stream and terminate PyAudio
        stream.stop_stream()
        stream.close()
        p.terminate()

def calculate_peak(data):
    # Convert raw audio data to a numpy array of int16
    samples = np.frombuffer(data, dtype=np.int16)
    # Calculate peak amplitude (maximum absolute sample value)
    peak_value = np.max(np.abs(samples))
    return peak_value

def capture_speech(recognizer, source) -> str:
    # Variable to hold the converted speech
    text = ""
    print("Listening...")
    recognized = False
    # recognizer.pause_threshold = 2.0
    while not recognized:
        try:
            audio = recognizer.listen(source)# , pause_threshold=2)
            print("Audio captured, now recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            recognized = True
        except sr.UnknownValueError:
            pass  # Ignore unknown value errors and continue listening
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            break  # Exit the loop in case of API errors
    return text
