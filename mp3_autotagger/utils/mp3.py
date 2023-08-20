import asyncio
import urllib.request
from pathlib import Path
from typing import Union

from mutagen.id3 import APIC, ID3, TALB, TCON, TDRC, TIT2, TPE1, ID3NoHeaderError
from mutagen.mp3 import MP3 as MP3_mutagen
from mutagen.mp3 import HeaderNotFoundError

from mp3_autotagger.utils.shazam import shazam_find_track_info


class MP3:
    """Class representing an MP3 file and its tags."""

    # Mapping of tag names to their respective classes in mutagen
    TAG_MAPPING = {"TPE1": TPE1, "TIT2": TIT2, "TALB": TALB, "TCON": TCON, "TDRC": TDRC, "APIC": APIC}

    def __init__(self, filepath: Path) -> None:
        """
        Initialize an MP3 object.

        Args:
            filepath (Path): Path to the MP3 file.
        """

        self._initialize_tags(filepath)
        self.filepath: Path = filepath
        self.supported_tags: list[str] = list(self.TAG_MAPPING.keys())
        self.tags: dict[str, Union[str, bytes]] = {
            tag_name: self._extract_tag(tag_name) for tag_name in self.supported_tags
        }

    def _initialize_tags(self, filepath: Path) -> None:
        """
        Initialize the audio tags for the MP3 file.

        Args:
            filepath (Path): Path to the MP3 file.
        """

        try:
            self.audiotags = ID3(filepath)
        except ID3NoHeaderError:
            # Handle the case where there's no ID3 header in the MP3 file
            try:
                mp3 = MP3_mutagen(filepath)
            except HeaderNotFoundError:  # Corrupted file
                raise
            mp3 = MP3_mutagen(filepath)
            mp3.add_tags()
            mp3.save()
            self.audiotags = ID3()

    def _extract_tag(self, tag_name: str) -> str | bytes:
        """
        Extract a specific tag's value from the audio tags.

        Args:
            tag_name (str): Name of the tag to extract.

        Returns:
            str | bytes: Extracted value of the tag.
        """

        if tag_name == "APIC":
            tag = self.audiotags.getall("APIC")
            tag = b"" if len(tag) == 0 else tag[0].data
        else:
            tag = self.audiotags.get(tag_name)
            if tag:
                tag = str(tag.text[0]) if tag_name == "TDRC" else tag.text[0]
            else:
                tag = ""

        return tag

    def _write_tag(self, tag_name: str, new_value: str | bytes) -> None:
        """
        Write a specific tag's value to the audio tags.

        Args:
            tag_name (str): Name of the tag to write.
            new_value (str | bytes): Value to write.
        """

        if tag_name == "APIC":
            # Handle album cover image
            self.audiotags.add(APIC(encoding=3, mime="image/jpeg", type=3, desc="Cover", data=new_value))
            return
        tag_class = self.TAG_MAPPING.get(tag_name)
        if tag_class:
            self.audiotags.add(tag_class(encoding=3, text=new_value))

    def update_tags_shazam(self, replace_existing_tags: bool = False) -> bool:
        """
        Update the MP3 tags using Shazam's track information.

        Args:
            replace_existing_tags (bool, optional): If True, replace existing tags. Defaults to False.

        Returns:
            bool: True if successful, False otherwise.
        """

        shazam_out = asyncio.run(shazam_find_track_info(self.filepath))

        if not shazam_out["matches"]:
            return False

        # Mapping of Shazam data to our tags
        shazam_data_mapping = {
            "TPE1": shazam_out["track"]["subtitle"].upper(),
            "TIT2": shazam_out["track"]["title"],
            "TALB": shazam_out["track"]["sections"][0]["metadata"][0]["text"],
            "TCON": shazam_out["track"]["genres"]["primary"],
            "TDRC": shazam_out["track"]["sections"][0]["metadata"][2]["text"],
            "APIC": urllib.request.urlopen(shazam_out["track"]["images"]["coverarthq"]).read(),
        }

        for tag_name, value in shazam_data_mapping.items():
            if replace_existing_tags or not self.tags[tag_name]:
                self.tags[tag_name] = value

        return True

    def save_as(self, new_filepath: Path = None) -> None:
        """
        Save the updated tags to the MP3 file.

        Args:
            new_filepath (Path, optional): If provided, rename the file to this path after saving. Defaults to None.
        """

        for tag_name, value in self.tags.items():
            self._write_tag(tag_name, value)
        self.audiotags.save(self.filepath, v2_version=3)

        if new_filepath:
            self.filepath.rename(new_filepath)
            self.filepath = new_filepath
