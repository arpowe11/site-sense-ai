"""
config.py

Configuration settings for the Flask app.
This includes debug mode, important paths, and extra parameters.

Used by:
    - app/__init__.py to initialize the settings
    - app/agent_logic.py for AI model and other paths

Author: Alexander Powell
Date: 2025-06-16
"""


from pathlib import Path

# FLASK CONFIGS
DEBUG: bool = True
HOST: str = "127.0.0.1"  # Use 127.0.0.1 for local and 0.0.0.0 for docker
PORT: int = 5000

# PATHS
BASE_DIR: Path = Path(__file__).resolve().parent.parent
TEMPLATES_DIR: Path = BASE_DIR / "app/sitesense/prompt_templates/prompt.txt"

# EXTRA
AI_MODEL: str = "gpt-4-turbo"
