import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Get the list of available voices
voices = engine.getProperty('voices')

# Loop through each voice and print its details
for voice in voices:
    print(f"Name: {voice.name}")
    print(f"ID: {voice.id}")
    print(f"Languages: {voice.languages}")
    print("-" * 20)