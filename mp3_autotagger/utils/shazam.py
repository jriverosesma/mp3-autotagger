from pathlib import Path
from typing import Any

from shazamio import Shazam

# Initialize a Shazam object globally
SHAZAM = Shazam()


async def shazam_find_track_info(filepath: Path) -> dict[str, Any]:
    """
    Use Shazam to recognize and retrieve information about a track from a given file path.

    Args:
        filepath (Path): The path to the audio file for which information is needed.

    Returns:
        dict[str, Any]: A dictionary containing information about the recognized track.
    """

    # Use Shazam's recognize_song method to identify the track from the provided filepath
    return await SHAZAM.recognize_song(filepath)
