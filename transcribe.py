import sys
import json
import wave
from vosk import Model, KaldiRecognizer
import os

try:
    # Get audio file path from command-line argument
    if len(sys.argv) != 2:
        print("Error: Please provide the audio file path")
        sys.exit(1)

    audio_file = sys.argv[1]

    # Use absolute path for model
    model_path = r"C:\Users\Aniket\Documents\GitHub\POC-Vosk\vosk-model-small-en-us-0.15"
    
    print(f"Loading model from: {model_path}")  # Debug print
    
    # Check if model directory exists and contains required files
    if not os.path.exists(model_path):
        print(f"Error: Model directory not found at {model_path}")
        sys.exit(1)
    
    if not os.path.exists(os.path.join(model_path, 'am')):
        print(f"Error: Model files missing in {model_path}")
        sys.exit(1)

    # Initialize model with absolute path
    model = Model(model_path)
    print("Model loaded successfully")  # Debug print

    # Open and check the audio file
    if not os.path.exists(audio_file):
        print(f"Error: Audio file not found at {audio_file}")
        sys.exit(1)

    wf = wave.open(audio_file, "rb")
    print(f"Audio file opened: {audio_file}")  # Debug print

    # Create recognizer
    rec = KaldiRecognizer(model, wf.getframerate())

    # Process audio file
    transcription = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            transcription += result["text"] + " "

    # Get final result
    final_result = json.loads(rec.FinalResult())
    transcription += final_result["text"]

    print(transcription.strip())

except Exception as e:
    print(f"Error: {str(e)}")
    sys.exit(1)
