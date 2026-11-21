import pyttsx3


VOICE_RATE = 175      # Speaking speed (smaller = slower)
VOICE_VOLUME = 1.0    # Volume: 0.0 to 1.0
VOICE_NUMBER = 0      # 0 = first installed voice, 1 = second voice, ...


def speak(text):
    """Speak the supplied text."""
    if not text or not text.strip():
        return

    try:
        # A fresh engine for every sentence. On many Windows computers a reused
        # engine speaks only the FIRST sentence and then stays silent.
        engine = pyttsx3.init()
        engine.setProperty("rate", VOICE_RATE)
        engine.setProperty("volume", VOICE_VOLUME)

        voices = engine.getProperty("voices")
        if voices and VOICE_NUMBER < len(voices):
            engine.setProperty("voice", voices[VOICE_NUMBER].id)

        engine.say(text)
        engine.runAndWait()
        engine.stop()

    except Exception as error:
        # If the speakers fail, the app keeps running (the text is still printed).
        print(f"Text-to-speech error: {error}")
