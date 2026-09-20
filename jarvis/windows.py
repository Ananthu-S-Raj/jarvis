"""Safe Windows and browser actions exposed to Jarvis."""

import os
import subprocess
import urllib.parse
import webbrowser

KNOWN_APPS = {
    "notepad": "notepad.exe", "calculator": "calc.exe", "calc": "calc.exe",
    "paint": "mspaint.exe", "explorer": "explorer.exe", "file explorer": "explorer.exe",
    "command prompt": "cmd.exe", "cmd": "cmd.exe",
}


def open_app(name: str) -> str:
    """Open a known Windows application or browser.

    Args:
        name: Application name, for example calculator, notepad, chrome, browser,
            WhatsApp, Microsoft Store, or file explorer.
    """
    key = name.lower().strip()
    if key in KNOWN_APPS:
        subprocess.Popen([KNOWN_APPS[key]])
        return f"Opened {name}."
    if key == "whatsapp":
        try:
            os.startfile("whatsapp:")
            return "Opened WhatsApp."
        except OSError:
            webbrowser.open("https://web.whatsapp.com/")
            return "Opened WhatsApp Web."
    if key in {"chrome", "browser", "google"}:
        webbrowser.open("https://www.google.com")
        return "Opened the browser."
    if key in {"microsoft store", "store"}:
        try:
            os.startfile("ms-windows-store:")
            return "Opened Microsoft Store."
        except OSError:
            return "Microsoft Store could not be opened."
    return f"Unknown application: {name}."


def close_app(name: str) -> str:
    """Close a known running Windows application.

    Args:
        name: Application name to close.
    """
    processes = {
        "calculator": "CalculatorApp.exe", "calc": "CalculatorApp.exe",
        "notepad": "notepad.exe", "paint": "mspaint.exe",
        "chrome": "chrome.exe", "browser": "chrome.exe", "whatsapp": "WhatsApp.exe",
    }
    key = name.lower().strip()
    process = processes.get(key)
    if not process:
        return f"Unknown application: {name}."
    result = subprocess.run(["taskkill", "/IM", process, "/F"], capture_output=True, text=True, check=False)
    return f"Closed {name}." if result.returncode == 0 else f"{name} was not found running."


def search_web(query: str) -> str:
    """Search the web in the default browser.

    Args:
        query: What to search for.
    """
    webbrowser.open("https://www.google.com/search?q=" + urllib.parse.quote_plus(query))
    return f"Searched the web for {query}."


def play_youtube(query: str) -> str:
    """Open YouTube search results for something the user wants to play.

    Args:
        query: Song, video, artist, topic, or other media to play.
    """
    webbrowser.open("https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(query))
    return f"Opened YouTube results for {query}."
