"""Gemini reasoning fallback for commands local tools cannot answer."""

from __future__ import annotations

import os

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
_client = None
_previous_interaction_id: str | None = None

SYSTEM_INSTRUCTION = """You are Jarvis, a concise Windows desktop assistant.
Local Python tools perform computer actions. You handle conversation and questions.
Never claim a computer action happened unless a local tool actually performed it.
Keep spoken answers concise unless the user asks for detail.
"""


def _get_client():
    global _client
    if _client is not None:
        return _client
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    from google import genai
    _client = genai.Client(api_key=api_key)
    return _client


def ask_gemini(message: str) -> str | None:
    global _previous_interaction_id
    client = _get_client()
    if client is None:
        return None
    try:
        interaction = client.interactions.create(
            model=MODEL,
            input=message,
            previous_interaction_id=_previous_interaction_id,
            system_instruction=SYSTEM_INSTRUCTION,
        )
        _previous_interaction_id = interaction.id
        answer = (interaction.output_text or "").strip()
        return answer or None
    except Exception as exc:
        print(f"Gemini error: {exc}")
        return None
