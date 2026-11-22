import os
from pathlib import Path
import sys


def rootpath():
    if home := os.getenv("AGENT_HOME"):
        return Path(home).expanduser().resolve()

    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    root = Path(__file__).resolve().parent.parent

    return root
