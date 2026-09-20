"""Gemini conversational fallback."""

from jarvis.config import GEMINI_API_KEY, GEMINI_MODEL

_client = None
_chat = None

SYSTEM_INSTRUCTION = """You are Jarvis, a concise Windows desktop assistant.
Local Python tools perform computer actions. You answer conversation and knowledge
questions. Never claim a computer action happened unless a local tool performed it.
Keep answers brief and natural because they are usually spoken aloud.
"""


def _get_chat():
    global _client, _chat
    if _chat is not None:
        return _chat
    if not GEMINI_API_KEY:
        return None

    from google import genai

    _client = genai.Client(api_key=GEMINI_API_KEY)
    _chat = _client.chats.create(model=GEMINI_MODEL)
    return _chat


def ask_gemini(message: str) -> str | None:
    chat = _get_chat()
    if chat is None:
        return None
    try:
        prompt = SYSTEM_INSTRUCTION + "\nUser: " + message
        response = chat.send_message(prompt)
        answer = (response.text or "").strip()
        return answer or None
    except Exception as exc:
        print(f"Gemini error: {exc}")
        return None
