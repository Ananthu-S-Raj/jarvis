"""Microphone input and speech recognition."""

import speech_recognition as sr


def listen() -> str | None:
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("\nListening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=10)

        print("Recognizing...")
        return recognizer.recognize_google(audio)

    except sr.WaitTimeoutError:
        print("No speech detected.")
    except sr.UnknownValueError:
        print("I couldn't understand that.")
    except sr.RequestError as exc:
        print(f"Speech recognition service error: {exc}")
    except OSError as exc:
        print(f"Microphone error: {exc}")

    return None
