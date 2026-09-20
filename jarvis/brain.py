"""Gemini reasoning and safe tool-calling layer."""

from jarvis.config import GEMINI_API_KEY, GEMINI_MODEL
from jarvis.windows import open_app, close_app, search_web, play_youtube

_client = None

SYSTEM_INSTRUCTION = """You are Jarvis, a concise Windows desktop assistant.
Use the supplied tools for computer/browser actions. You may chain tools when needed.
Never claim an action happened unless a tool result says it happened.
For requests to play a song/video, use play_youtube. If the user asks to open a browser
and then do something, perform the useful browser action instead of treating the entire
phrase as an application name. Keep final replies short because they may be spoken.
"""


def _client_or_none():
    global _client
    if _client is not None:
        return _client
    if not GEMINI_API_KEY:
        return None
    from google import genai
    _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client


def ask_gemini(message: str, with_tools: bool = False) -> str | None:
    client = _client_or_none()
    if client is None:
        return None
    try:
        from google.genai import types
        tools = [open_app, close_app, search_web, play_youtube] if with_tools else None
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=message,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                tools=tools,
            ),
        )
        answer = (response.text or "").strip()
        return answer or None
    except Exception as exc:
        print(f"Gemini error: {exc}")
        return None
