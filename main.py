"""The voice app: listen -> ask the LangGraph AI -> speak the answer."""

# PHASE 1 (simple chatbot):        from chat_graph import ask_ai
# PHASE 2 (coding assistant):      from coding_graph import ask_ai
from coding_graph import ask_ai

from voice_input import listen
from voice_output import speak


EXIT_WORDS = {"exit", "stop", "quit", "goodbye"}


def main():
    print("\nVoice AI Assistant is ready!  Say 'exit' to close.")
    speak("Hello! I am ready. What would you like me to do?")

    while True:
        try:
            user_text = listen()
            if not user_text:
                continue                      # nothing heard, listen again

            print(f"\nYou: {user_text}")

            if user_text.lower().strip(" .!?") in EXIT_WORDS:
                speak("Goodbye! Have a great day.")
                break

            print("Thinking...")
            answer = ask_ai(user_text)
            print(f"\nAssistant: {answer}")
            speak(answer)

        except KeyboardInterrupt:
            print("\nStopped by keyboard.")
            break

        except Exception as error:
            print(f"\nSomething went wrong: {error}")
            speak("Sorry, something went wrong. Please check the screen.")


if __name__ == "__main__":
    main()
