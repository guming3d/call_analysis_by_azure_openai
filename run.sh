#!/bin/bash

# Navigate to the audio_transcription directory
cd audio_transcription

# a) Install dependencies
pip install -r requirements.txt --user

# b) Run the code
python3 src/main.py
