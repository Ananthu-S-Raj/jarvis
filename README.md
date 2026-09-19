# Jarvis

A voice-first Windows desktop buddy.

## Phase 1

The first milestone proves the core loop:

**microphone -> speech recognition -> command routing -> Windows/browser action -> spoken response**

Current commands include:

- "Open Notepad"
- "Open Calculator"
- "Open Paint"
- "Open Chrome"
- "Search Google for Spring Boot microservices"
- "Hello Jarvis"
- "Exit"

## Local setup (Windows)

Clone the repository:

```powershell
git clone https://github.com/Ananthu-S-Raj/jarvis.git
cd jarvis
```

Create a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell activation is restricted, use Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run Jarvis:

```powershell
python main.py
```

Allow microphone access if Windows asks.

## Important

Phase 1 deliberately has no LLM and no always-on wake word. We first verify that microphone input, speech recognition, Windows actions, and speech output work reliably. Later phases will add a wake word, UI, tool-based AI agent, memory, browser automation, and screen awareness.

Never commit API keys or passwords. Local secrets will go in a `.env` file, which is ignored by Git.
