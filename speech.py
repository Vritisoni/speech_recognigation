import pyaudio
import threading
import azure.cognitiveservices.speech as speechsdk
from googletrans import Translator
import pyttsx3
import tkinter as tk
from tkinter import messagebox

import threading
import time
import azure.cognitiveservices.speech as speechsdk
from googletrans import Translator
import pyttsx3

# Flag to stop the program after processing one speech input
program_running = True

# Event to signal the completion of TTS
tts_completed_event = threading.Event()

# Azure Speech Recognizer setup
def setup_speech_recognizer():
    speech_key = "Fef2ZjHiA4Dc3D6q1SwJBk6kpYmmxnznr2t2A4PPhLAs53B45SNkJQQJ99ALACmepeSXJ3w3AAAAACOGurOb"
    region = "uksouth"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)
    speech_config.speech_recognition_language = "en-US"
    return speechsdk.SpeechRecognizer(speech_config=speech_config)

# Faster Text-to-Speech (TTS) using pyttsx3
def local_text_to_speech(text):
    try:
        engine = pyttsx3.init()
        
        # Define a callback to signal when TTS is completed
        def on_end_speaking(name, completed):
            if completed:
                tts_completed_event.set()  # Signal TTS completion

        # Attach the callback
        engine.connect('finished-utterance', on_end_speaking)
        
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Local TTS error: {e}")
        tts_completed_event.set()  # Signal TTS completion even if there's an error

# Translate text using Google Translate API
def translate_text(text, target_language='en'):
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text

# Real-time speech-to-text processing
def siri_like_processing(speech_recognizer):
    def on_recognizing(event):
        """Handle partial speech recognition results."""
        if event.result.reason == speechsdk.ResultReason.RecognizingSpeech:
            partial_text = event.result.text
            print(f"Partial Recognition: {partial_text}", end="\r")  # Update dynamically on the same line

    def on_recognized(event):
        """Handle final speech recognition results."""
        global program_running

        if event.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            original_text = event.result.text
            print(f"\nRecognized: {original_text}")

            # Translate text
            translated_text = translate_text(original_text)
            print(f"Translated: {translated_text}")

            # Respond via TTS
            tts_completed_event.clear()  # Reset the event before starting TTS
            local_text_to_speech(translated_text)

            # Wait for TTS to complete
            tts_completed_event.wait()

            # Stop the program and the recognizer after completing the TTS
            speech_recognizer.stop_continuous_recognition()
            program_running = False

        elif event.result.reason == speechsdk.ResultReason.NoMatch:
            print("I didn't catch that. Try again.")
        elif event.result.reason == speechsdk.ResultReason.Canceled:
            print("Recognition canceled.")

    # Connect the events to their handlers
    speech_recognizer.recognizing.connect(on_recognizing)  # Real-time updates
    speech_recognizer.recognized.connect(on_recognized)   # Final result

# Start speech recognition
def start_speech_assistant():
    global program_running

    recognizer = setup_speech_recognizer()
    siri_like_processing(recognizer)

    print("Listening for speech... Press Ctrl+C to stop.")
    recognizer.start_continuous_recognition()

    try:
        while program_running:
            time.sleep(0.1)  # Keep the process alive

    except KeyboardInterrupt:
        print("\nSpeech recognition stopped by user.")

    finally:
        recognizer.stop_continuous_recognition()
        print("\nProgram terminated.")

if __name__ == "__main__":
    start_speech_assistant()
