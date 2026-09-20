"""Jarvis desktop buddy launcher."""

import sys


def main():
    if "--cli" in sys.argv:
        from jarvis.commands import handle_command, should_exit
        from jarvis.speaker import speak
        from jarvis.voice import listen
        print("Jarvis CLI ready.")
        try:
            while True:
                command=listen()
                if not command:
                    continue
                print(f"You: {command}")
                if should_exit(command):
                    speak("Goodbye.")
                    break
                response=handle_command(command)
                print(f"Jarvis: {response}")
                speak(response)
        except KeyboardInterrupt:
            print("\nJarvis stopped.")
    else:
        from jarvis.ui import run_ui
        run_ui()


if __name__ == "__main__":
    main()
