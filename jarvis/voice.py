"""Microphone input and speech recognition."""

import speech_recognition as sr

_recognizer = sr.Recognizer()
_recognizer.dynamic_energy_threshold = True
_recognizer.pause_threshold = 0.7


def listen() -> str | None:
    try:
        with sr.Microphone() as source:
            print("\nListening...")
            audio = _recognizer.listen(source, timeout=8, phrase_time_limit=12)

        print("Recognizing...")
        return _recognizer.recognize_google(audio)

    except sr.WaitTimeoutError:
        print("No speech detected.")
    except sr.UnknownValueError:
        print("I couldn't understand that.")
    except sr.RequestError as exc:
        print(f"Speech recognition service error: {exc}")
    except OSError as exc:
        print(f"Microphone error: {exc}")
    except KeyboardInterrupt:
        raise

    return None
