from pathlib import Path
from typing import Any

from shazamio import Shazam

shazam = Shazam()


async def shazam_find_track_info(filepath: Path) -> dict[str, Any]:
    return await shazam.recognize_song(filepath)
