import sounddevice as sd
import speech_recognition as sr


# Speech language: "en-IN" (Indian English), "en-US", or "hi-IN" (Hindi).
LANGUAGE = "en-IN"

RECORD_SECONDS = 5     # How long to record after "Listening..."
SAMPLE_RATE = 16000    # 16000 sound samples per second is enough for speech

# Leave as None to use the default microphone.
# Run list_microphones.py to see the numbers if you need a different microphone.
MICROPHONE_INDEX = None


def listen():
    """Record from the mic and return the text. Return None if not understood."""
    try:
        print(f"\nListening for {RECORD_SECONDS} seconds... Speak now.")
        recording = sd.rec(
            int(RECORD_SECONDS * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="int16",
            device=MICROPHONE_INDEX
        )
        sd.wait()  # wait until the recording is finished

        # Put the recorded sound into the format SpeechRecognition understands.
        audio = sr.AudioData(recording.tobytes(), SAMPLE_RATE, 2)

        print("Recognizing your speech...")
        text = sr.Recognizer().recognize_google(audio, language=LANGUAGE)
        return text.strip()

    except sr.UnknownValueError:
        print("Sorry, I could not understand. Please speak again.")

    except sr.RequestError as error:
        print(f"Speech recognition service error (check internet): {error}")

    except sd.PortAudioError as error:
        # No microphone found: stop the app with a clear message.
        raise SystemExit(f"Microphone error: {error}. Check your mic settings.")

    except Exception as error:
        print(f"Unexpected voice input error: {error}")

    return None
