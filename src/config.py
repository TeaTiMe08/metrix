import os

from file_utils import FileUtils


class Config:
    """Class to handle configuration and environment variables."""

    # Debug Mode
    DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

    # Authentication
    TOKEN = os.getenv("GITHUB_TOKEN") if not DEBUG_MODE else FileUtils.read_token_from_file()
    GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "joanroig")

    # Fonts
    FONT_PATH = os.getenv("FONT_PATH", "assets/MxPlus_IBM_BIOS.ttf")
    SYMBOL_FONT_PATH = os.getenv("SYMBOL_FONT_PATH", "assets/MxPlus_IBM_BIOS.ttf")

    # Colors
    TEXT_COLOR = os.getenv("TEXT_COLOR", "limegreen")
    BACKGROUND_COLOR = os.getenv("BACKGROUND_COLOR", "black")

    # Content Settings
    TITLE_SUFFIX = os.getenv("TITLE_SUFFIX", "'s GitHub Metrix")
    ACTIVITY_TEXT = os.getenv("ACTIVITY_TEXT", "Last month commit activity:")
    ACTIVITY_DAYS = int(os.getenv("ACTIVITY_DAYS", 30))

    # Display Settings
    LOOP = 0 if os.getenv("LOOP", "false").lower() == "true" else -1
    WIDTH = int(os.getenv("WIDTH", 622))
    HEIGHT = int(os.getenv("HEIGHT", 350))

    # Glitch Effect
    GLITCHES = os.getenv("GLITCHES", "true").lower() == "true"
    GLITCH_SYMBOLS = ['☺', '☻', '♥', '♦', '♣', '♠', '•', '◘', '○', '◙', '█', '░', '▒', '▓', '☼', '♪', '♫', '■', '□', '▲', '►', '▼', '◄', '◊', '●']

    # Output Paths
    OUTPUT_GIF = "metrix.gif"
    TEMP_FRAMES_DIR = "frames"
