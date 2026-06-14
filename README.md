# Local Text-to-Speech MCP Server

A lightweight, local [Model Context Protocol](https://modelcontextprotocol.io)
(MCP) server that exposes a text-to-speech tool. An AI assistant (such as
Claude Code) can send its written task summaries to the tool, which reads them
aloud instantly using your computer's native, **offline** speech engine.

Because the speech engine ([`pyttsx3`](https://pypi.org/project/pyttsx3/)) runs
entirely on your machine, there is near-zero latency and no network calls.

## Features

- `speak_text(text, rate=175, volume=1.0)` — read text aloud through the
  native OS voice. `rate` (words per minute) and `volume` (0.0–1.0) are
  optional overrides.
- `list_voices()` — enumerate the voices installed on the local system.

## Requirements

- Python 3.10+
- A working native speech engine:
  - **macOS:** built in (NSSpeechSynthesizer) — no setup needed.
  - **Windows:** built in (SAPI5) — no setup needed.
  - **Linux:** install `espeak`/`espeak-ng` and ALSA, e.g.
    `sudo apt-get install espeak-ng libespeak1`.

## Setup

```bash
# 1. Clone and enter the project
cd tts-mcp

# 2. Create and activate a virtual environment
python -m venv venv

# macOS/Linux:
source venv/bin/activate
# Windows (Command Prompt):
venv\Scripts\activate.bat
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt
```

## Local testing

Verify the server starts without errors:

```bash
python server.py
```

It runs over stdio and stays active. Press `Ctrl+C` to stop it.

To exercise the tools interactively, use the MCP Inspector:

```bash
mcp dev server.py
```

## Integrate with Claude Code / other MCP clients

Add the server to your MCP configuration (e.g. `.mcp.json` in your project or
your client's global config). See [`mcp.json.example`](./mcp.json.example):

```json
{
  "mcpServers": {
    "local-tts": {
      "command": "/absolute/path/to/tts-mcp/venv/bin/python",
      "args": ["/absolute/path/to/tts-mcp/server.py"]
    }
  }
}
```

Replace `/absolute/path/to/` with your actual local paths. On Windows the
command is typically `...\venv\Scripts\python.exe`.

You can also register it with the Claude Code CLI:

```bash
claude mcp add local-tts /absolute/path/to/tts-mcp/venv/bin/python /absolute/path/to/tts-mcp/server.py
```

## Prompting strategy

Tell your assistant that when a task is finished it should structure its
response into concise bullet points and call `speak_text` with that summary —
for example: "When you say *Task complete*, summarize the work as short bullet
points and read it aloud with the `speak_text` tool."

## License

MIT
