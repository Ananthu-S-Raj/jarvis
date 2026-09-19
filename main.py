"""Jarvis desktop buddy entry point."""

from jarvis.commands import handle_command, should_exit
from jarvis.speaker import speak
from jarvis.voice import listen


def main() -> None:
    speak("Jarvis is ready.")
    print("Jarvis is ready. Say 'Hey Jarvis' followed by a command.")

    try:
        while True:
            command = listen()
            if not command:
                continue

            print(f"You: {command}")

            if should_exit(command):
                print("Jarvis: Goodbye.")
                speak("Goodbye.")
                break

            response = handle_command(command)
            print(f"Jarvis: {response}")
            speak(response)

    except KeyboardInterrupt:
        print("\nJarvis: Stopped.")
        speak("Goodbye.")


if __name__ == "__main__":
    main()
