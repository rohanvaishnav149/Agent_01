from voice_input import listen

text = listen()

if text:
    print("Recognized text:", text)
else:
    print("No text was recognized.")
