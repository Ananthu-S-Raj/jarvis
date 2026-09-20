"""Hybrid fast local router with Gemini tool planning."""

from datetime import datetime, timedelta
import re

from jarvis.brain import ask_gemini
from jarvis.notes import add_note, recent_notes
from jarvis.windows import close_app, open_app, search_web, play_youtube

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

    # Only intercept simple single-action app commands. Compound language goes to Gemini.
    match=re.fullmatch(r"(?:open|launch|start)\s+(?:the\s+)?([\w ]+)",command)
    if match and not any(word in command for word in (" and ", " then ", " play ", " search ", " for ")):
        return open_app(match.group(1).strip())

    match=re.fullmatch(r"(?:close|quit|stop)\s+(?:the\s+)?([\w ]+)",command)
    if match and " and " not in command and " then " not in command:
        return close_app(match.group(1).strip())

    match=re.fullmatch(r"(?:search(?: google)?(?: for)?|google)\s+(.+)",command)
    if match:
        return search_web(match.group(1).strip())

    match=re.fullmatch(r"(?:play|play youtube|youtube)\s+(.+)",command)
    if match:
        return play_youtube(match.group(1).strip())

    match=re.fullmatch(r"(?:create|add|save|make) (?:a )?note(?: saying| that|:)?\s+(.+)",command)
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
    answer=ask_gemini(command, with_tools=True)
    if answer:
        return answer
    return "My AI connection is unavailable, and I don't have a local tool for that yet."
