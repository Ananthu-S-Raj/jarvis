"""Simple Phase 1 command router for Windows."""

import subprocess
import urllib.parse
import webbrowser


def _open_windows_app(command: str) -> str | None:
    apps = {
        "notepad": ("notepad.exe", "Opening Notepad."),
        "calculator": ("calc.exe", "Opening Calculator."),
        "paint": ("mspaint.exe", "Opening Paint."),
    }

    for name, (executable, response) in apps.items():
        if f"open {name}" in command:
            subprocess.Popen([executable])
            return response

    return None


def handle_command(raw_command: str) -> str:
    command = raw_command.lower().strip()

    app_response = _open_windows_app(command)
    if app_response:
        return app_response

    if "open chrome" in command:
        # Using the default browser keeps Phase 1 portable even when Chrome's
        # installation path differs between Windows machines.
        webbrowser.open("https://www.google.com")
        return "Opening your browser."

    search_prefixes = (
        "search google for ",
        "google ",
        "search for ",
        "search ",
    )
    for prefix in search_prefixes:
        if command.startswith(prefix):
            query = raw_command[len(prefix):].strip()
            if query:
                encoded = urllib.parse.quote_plus(query)
                webbrowser.open(f"https://www.google.com/search?q={encoded}")
                return f"Searching Google for {query}."

    if command in {"hello", "hello jarvis", "hi jarvis"}:
        return "Hello. How can I help?"

    return "I don't know that command yet."
