from pathlib import Path
from typing import Any, Callable, Optional, Union

import yt_dlp as ydl


def get_youtube_audiostream(
    url: str,
    save_dirpath: Path = Path("."),
    download: bool = True,
    quiet: bool = True,
    callback: Optional[Callable] = None,
    convert_to_mp3: bool = False,
) -> Union[dict[str, Any], None]:
    ydl_opts = {
        "quiet": quiet,
        "format": "bestaudio/best",
        "noplaylist": True,
        "progress_hooks": [callback] if callback else [],
        "outtmpl": str(save_dirpath / "%(title)s.%(ext)s"),
    }

    if convert_to_mp3:
        ydl_opts["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }
        ]

    with ydl.YoutubeDL(ydl_opts) as y:
        info = y.extract_info(url, download=download)

    return info
