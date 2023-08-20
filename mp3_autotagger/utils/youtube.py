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
    """
    Extract audio stream information from a given YouTube URL and optionally download it.

    Args:
        url (str): The YouTube video URL.
        save_dirpath (Path, optional): Directory path where the audio stream should be saved.
            Defaults to the current directory.
        download (bool, optional): Whether to download the audio stream. Defaults to True.
        quiet (bool, optional): If True, yt_dlp will not print any messages to stdout. Defaults to True.
        callback (Optional[Callable], optional): A function to be called as a progress hook.
            Defaults to None.
        convert_to_mp3 (bool, optional): If True, the downloaded audio stream will be converted to MP3.
            Defaults to False.

    Returns:
        Union[dict[str, Any], None]: A dictionary containing the extracted information of the audio
            stream or None if extraction fails.
    """

    # Set yt_dlp options
    ydl_opts = {
        "quiet": quiet,  # Suppress output messages if 'quiet' is True
        "format": "bestaudio/best",  # Choose the best quality audio
        "noplaylist": True,  # Ensure only single video is processed, not playlists
        "progress_hooks": [callback] if callback else [],  # Set progress hooks if provided
        "outtmpl": str(save_dirpath / "%(title)s.%(ext)s"),  # Define the output template for the saved audio
    }

    # If converting to MP3, add postprocessors options to the dictionary
    if convert_to_mp3:
        ydl_opts["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }
        ]

    # Use yt_dlp to extract the information
    with ydl.YoutubeDL(ydl_opts) as y:
        info = y.extract_info(url, download=download)

    return info
