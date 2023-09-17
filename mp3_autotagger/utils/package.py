import sys


def is_running_as_pyinstaller_bundle() -> bool:
    """Check if application is running as a `PyInstaller` bundle."""

    return hasattr(sys, "_MEIPASS")
