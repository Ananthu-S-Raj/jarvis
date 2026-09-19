"""Text-to-speech output."""

import pyttsx3


_engine = None


def _get_engine():
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
        _engine.setProperty("rate", 180)
    return _engine


def speak(text: str) -> None:
    engine = _get_engine()
    engine.say(text)
    engine.runAndWait()
