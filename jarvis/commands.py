"""Hybrid local command router with Gemini fallback."""

from datetime import datetime, timedelta
import re
import urllib.parse
import webbrowser

from jarvis.brain import ask_gemini
from jarvis.notes import add_note, recent_notes
from jarvis.windows import close_app, open_app

WAKE_PATTERNS=(r"^hey\s+jarvis\b[,:]?\s*",r"^hi\s+jarvis\b[,:]?\s*",r"^okay\s+jarvis\b[,:]?\s*",r"^ok\s+jarvis\b[,:]?\s*",r"^jarvis\b[,:]?\s*")
EXIT_PHRASES=("exit","quit","goodbye","bye jarvis","exit jarvis","close jarvis","stop jarvis")


def normalize_command(raw):
    command=raw.lower().strip()
    for pattern in WAKE_PATTERNS:
        command=re.sub(pattern,"",command,count=1)
    return re.sub(r"\s+"," ",command).strip()


def should_exit(raw):
    command=normalize_command(raw)
    return any(command==p or command.startswith(p+" ") for p in EXIT_PHRASES)


def _local(command):
    if not command:
        return "Yes?"

    if command in {"hello","hi","hey"}:
        return "Hello. How can I help?"

    match=re.search(r"\b(?:open|launch|start)\s+(?:the\s+)?(.+)$",command)
    if match:
        return open_app(match.group(1).strip())

    match=re.search(r"\b(?:close|quit|stop)\s+(?:the\s+)?(.+)$",command)
    if match:
        return close_app(match.group(1).strip())

    match=re.search(r"^(?:search(?: google)?(?: for)?|google)\s+(.+)$",command)
    if match:
        query=match.group(1).strip()
        webbrowser.open("https://www.google.com/search?q="+urllib.parse.quote_plus(query))
        return f"Searching Google for {query}."

    match=re.search(r"^(?:create|add|save|make) (?:a )?note(?: saying| that|:)?\s+(.+)$",command)
    if match:
        return add_note(match.group(1).strip())

    if command in {"show notes","read notes","my notes","recent notes"}:
        notes=recent_notes()
        return "Your recent notes are: "+". ".join(notes) if notes else "You don't have any notes yet."

    now=datetime.now()
    if "time" in command:
        return f"It is {now.strftime('%I:%M %p').lstrip('0')}."
    if "tomorrow" in command and ("date" in command or "day" in command):
        d=now+timedelta(days=1)
        return f"Tomorrow is {d.strftime('%A, %B %d, %Y')}."
    if "date" in command or command=="today":
        return f"Today is {now.strftime('%A, %B %d, %Y')}."

    return None


def handle_command(raw_command):
    command=normalize_command(raw_command)
    local=_local(command)
    if local:
        return local
    answer=ask_gemini(command)
    if answer:
        return answer
    return "I understood you, but my AI connection is unavailable and I don't have a local tool for that yet."
