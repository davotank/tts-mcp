"""Local Text-to-Speech MCP server.

Exposes a `speak_text` tool over the Model Context Protocol so an AI
assistant can have its written summaries read aloud using the machine's
native, offline speech engine (via pyttsx3).
"""

import logging

import pyttsx3
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-local-tts")

mcp = FastMCP("Local TTS Server")


@mcp.tool()
def speak_text(text: str, rate: int = 175, volume: float = 1.0) -> str:
    """Read text aloud using the local system voice.

    :param text: The text content or summary to be spoken.
    :param rate: Speech rate in words per minute (default 175).
    :param volume: Volume level from 0.0 to 1.0 (default 1.0).
    """
    if not text.strip():
        return "Error: No text provided to speak."

    try:
        # Initialise the engine inside the tool call so each invocation gets a
        # clean run/wait loop and the audio thread does not stay blocked.
        logger.info("Initializing native TTS engine...")
        engine = pyttsx3.init()

        engine.setProperty("rate", rate)
        engine.setProperty("volume", max(0.0, min(1.0, volume)))

        logger.info("Speaking text: %s...", text[:50])
        engine.say(text)
        engine.runAndWait()
        engine.stop()

        return "Audio playback completed successfully."
    except Exception as e:  # noqa: BLE001 - report any engine failure back to the client
        logger.error("TTS execution failed: %s", e)
        return f"Failed to play audio locally. Error: {e}"


@mcp.tool()
def list_voices() -> str:
    """List the voices available on the local system speech engine."""
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty("voices")
        engine.stop()
        if not voices:
            return "No voices found on the local system."
        lines = [
            f"{i}: {v.name} (id={v.id})"
            for i, v in enumerate(voices)
        ]
        return "Available voices:\n" + "\n".join(lines)
    except Exception as e:  # noqa: BLE001
        logger.error("Failed to enumerate voices: %s", e)
        return f"Failed to list voices. Error: {e}"


if __name__ == "__main__":
    # Run the server using stdio transport.
    mcp.run(transport="stdio")
