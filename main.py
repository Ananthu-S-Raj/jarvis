"""Jarvis Phase 1 entry point."""

from jarvis.commands import handle_command
from jarvis.speaker import speak
from jarvis.voice import listen


def main() -> None:
    speak("Jarvis phase one is ready.")
    print("Jarvis is ready. Say a command, or say 'exit' to stop.")

    while True:
        command = listen()
        if not command:
            continue

        print(f"You: {command}")
        if command.lower().strip() in {"exit", "quit", "stop jarvis", "goodbye"}:
            speak("Goodbye.")
            break

        response = handle_command(command)
        print(f"Jarvis: {response}")
        speak(response)


if __name__ == "__main__":
    main()
