"""Safe Windows desktop actions."""

import os
import subprocess
import webbrowser


KNOWN_APPS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "calc": "calc.exe",
    "paint": "mspaint.exe",
    "explorer": "explorer.exe",
    "file explorer": "explorer.exe",
    "command prompt": "cmd.exe",
    "cmd": "cmd.exe",
}


def open_app(name: str) -> str:
    key = name.lower().strip()
    if key in KNOWN_APPS:
        subprocess.Popen([KNOWN_APPS[key]])
        return f"Opening {name}."

    if key == "whatsapp":
        try:
            os.startfile("whatsapp:")
            return "Opening WhatsApp."
        except OSError:
            webbrowser.open("https://web.whatsapp.com/")
            return "Opening WhatsApp Web."

    if key in {"chrome", "browser", "google"}:
        webbrowser.open("https://www.google.com")
        return "Opening your browser."

    if key in {"microsoft store", "store"}:
        try:
            os.startfile("ms-windows-store:")
            return "Opening Microsoft Store."
        except OSError:
            return "I couldn't open Microsoft Store."

    return f"I don't know how to open {name} yet."


def close_app(name: str) -> str:
    processes = {
        "calculator": "CalculatorApp.exe",
        "calc": "CalculatorApp.exe",
        "notepad": "notepad.exe",
        "paint": "mspaint.exe",
        "chrome": "chrome.exe",
        "whatsapp": "WhatsApp.exe",
    }
    key = name.lower().strip()
    process = processes.get(key)
    if not process:
        return f"I don't know how to close {name} yet."

    result = subprocess.run(
        ["taskkill", "/IM", process, "/F"],
        capture_output=True,
        text=True,
        check=False,
    )
    return f"Closed {name}." if result.returncode == 0 else f"I couldn't find {name} running."
