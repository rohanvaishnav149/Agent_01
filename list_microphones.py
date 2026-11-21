import sounddevice as sd

# Prints every sound device with its number.
# Microphones have "in" channels more than 0.
# Put the right number in MICROPHONE_INDEX inside voice_input.py if needed.
print(sd.query_devices())
