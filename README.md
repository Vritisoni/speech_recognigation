# Phase 2: Real-Time Audio Streaming & Translation

This project implements real-time audio capture, streaming, translation, and playback functionality. It captures audio from a speaker, processes it in real time using Microsoft's Speech-to-Text (STT) and translation services, and streams the translated audio back to attendees using Text-to-Speech (TTS).

---

## Features

- **Real-Time Audio Capture:** Captures audio from the speaker and streams it to the backend.
- **Speech-to-Text (STT):** Converts spoken audio to text using Microsoft STT.
- **Translation:** Translates text into the desired language.
- **Text-to-Speech (TTS):** Converts translated text into audio and streams it back to attendees.

---

## Technology Stack

- **Frontend:**
  - Audio capture (e.g., WebRTC or microphone interface).
- **Backend:**
  - Microsoft STT and TTS integration.
  - Translation service (Microsoft Translator or similar).
  - WebSocket/HTTP for real-time streaming.
- **Tools and Libraries:**
  - Python, Node.js, or your preferred backend language.
  - Microsoft Azure Cognitive Services.
  - WebSocket or other streaming protocols.

---

## Installation
run : python speech.py

### Prerequisites

1. Install Python 3.8+ or Node.js, depending on the backend implementation.
2. Create an Azure account and set up Microsoft Speech-to-Text (STT), Translation, and Text-to-Speech (TTS) services.
3. Install required dependencies.


