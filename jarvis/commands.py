"""Rule-based desktop tools used before the LLM layer is added."""

from __future__ import annotations

from datetime import datetime, timedelta
import os
import re
import subprocess
import urllib.parse
import webbrowser


WAKE_PATTERNS = (
    r"^hey\s+jarvis\b[,:]?\s*",
    r"^hi\s+jarvis\b[,:]?\s*",
    r"^okay\s+jarvis\b[,:]?\s*",
    r"^ok\s+jarvis\b[,:]?\s*",
    r"^jarvis\b[,:]?\s*",
)

EXIT_PHRASES = (
    "exit",
    "quit",
    "goodbye",
    "bye jarvis",
    "exit jarvis",
    "close jarvis",
    "stop jarvis",
    "shutdown jarvis",
)


def normalize_command(raw_command: str) -> str:
    command = raw_command.lower().strip()
    for pattern in WAKE_PATTERNS:
        command = re.sub(pattern, "", command, count=1)
    command = re.sub(r"\s+", " ", command).strip()
    return command


def should_exit(raw_command: str) -> bool:
    command = normalize_command(raw_command)
    return any(
        command == phrase or command.startswith(f"{phrase} ")
        for phrase in EXIT_PHRASES
    )


def _open_app(command: str) -> str | None:
    apps = {
        "notepad": ("notepad.exe", "Opening Notepad."),
        "calculator": ("calc.exe", "Opening Calculator."),
        "calc": ("calc.exe", "Opening Calculator."),
        "paint": ("mspaint.exe", "Opening Paint."),
        "file explorer": ("explorer.exe", "Opening File Explorer."),
        "explorer": ("explorer.exe", "Opening File Explorer."),
        "command prompt": ("cmd.exe", "Opening Command Prompt."),
        "cmd": ("cmd.exe", "Opening Command Prompt."),
    }

    if not re.search(r"\b(open|launch|start)\b", command):
        return None

    for name, (executable, response) in apps.items():
        if name in command:
            subprocess.Popen([executable])
            return response

    if "whatsapp" in command:
        try:
            os.startfile("whatsapp:")
            return "Opening WhatsApp."
        except OSError:
            webbrowser.open("https://web.whatsapp.com/")
            return "Opening WhatsApp Web."

    if any(name in command for name in ("chrome", "browser", "google")):
        webbrowser.open("https://www.google.com")
        return "Opening your browser."

    return None


def _close_app(command: str) -> str | None:
    if not re.search(r"\b(close|quit|exit|kill|stop)\b", command):
        return None

    processes = {
        "calculator": ("CalculatorApp.exe", "Closing Calculator."),
        "calc": ("CalculatorApp.exe", "Closing Calculator."),
        "notepad": ("notepad.exe", "Closing Notepad."),
        "paint": ("mspaint.exe", "Closing Paint."),
        "chrome": ("chrome.exe", "Closing Chrome."),
        "whatsapp": ("WhatsApp.exe", "Closing WhatsApp."),
    }

    for name, (process, response) in processes.items():
        if name in command:
            result = subprocess.run(
                ["taskkill", "/IM", process, "/F"],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0:
                return response
            return f"I couldn't find a running {name} window."

    return None


def _search_web(raw_command: str, command: str) -> str | None:
    match = re.search(
        r"^(?:please\s+)?(?:search(?:\s+google)?(?:\s+for)?|google)\s+(.+)$",
        command,
    )
    if not match:
        return None

    query = match.group(1).strip()
    if not query:
        return "What should I search for?"

    webbrowser.open(
        "https://www.google.com/search?q=" + urllib.parse.quote_plus(query)
    )
    return f"Searching Google for {query}."


def _date_time(command: str) -> str | None:
    now = datetime.now()

    if "time" in command and re.search(r"\b(what|tell|current|time)\b", command):
        return f"It is {now.strftime('%I:%M %p').lstrip('0')}."

    if "tomorrow" in command and ("date" in command or "day" in command):
        tomorrow = now + timedelta(days=1)
        return f"Tomorrow is {tomorrow.strftime('%A, %B %d, %Y')}."

    if "date" in command or "today" in command:
        return f"Today is {now.strftime('%A, %B %d, %Y')}."

    return None


def _calculate(command: str) -> str | None:
    expression = command
    expression = re.sub(r"^(what(?:'s| is)?|calculate|compute)\s+", "", expression)
    replacements = {
        "plus": "+",
        "minus": "-",
        "times": "*",
        "multiplied by": "*",
        "x": "*",
        "divided by": "/",
        "over": "/",
    }
    for word, symbol in replacements.items():
        expression = expression.replace(word, symbol)

    expression = expression.replace("?", "").strip()
    if not re.fullmatch(r"[0-9+\-*/().\s]+", expression):
        return None

    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"The answer is {result}."
    except (SyntaxError, ZeroDivisionError, TypeError):
        return "I couldn't calculate that expression."


def handle_command(raw_command: str) -> str:
    command = normalize_command(raw_command)

    if not command:
        return "Yes?"

    if command in {"hello", "hi", "hey"}:
        return "Hello. How can I help?"

    for handler in (_close_app, _open_app):
        response = handler(command)
        if response:
            return response

    response = _search_web(raw_command, command)
    if response:
        return response

    response = _date_time(command)
    if response:
        return response

    response = _calculate(command)
    if response:
        return response

    if "who am i" in command:
        return "I don't know enough about you yet. Memory will be added in a later phase."

    return "I heard you, but I don't have a tool for that yet."
