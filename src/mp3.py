import os
import asyncio
import urllib.request

from mutagen.id3 import ID3, ID3NoHeaderError, TPE1, TIT2, TALB, TCON, TDRC, APIC
from mutagen.mp3 import MP3 as MP3_mutagen, HeaderNotFoundError

from src.utils import shazam_find_track_info


class MP3:

    def __init__(self, filepath):
        try:
            self.audiotags = ID3(filepath)
        except ID3NoHeaderError:
            try:
                mp3 = MP3_mutagen(filepath)
            except HeaderNotFoundError: # Corrupted file
                raise
            mp3.add_tags()
            mp3.save()
            self.audiotags = ID3()

        self.filepath = filepath
        self.supported_tags = ['TPE1', 'TIT2', 'TALB', 'TCON', 'TDRC', 'APIC']
        self.tags = {}

        for tag_name in self.supported_tags:
            self.tags[tag_name] = self._extract_tag(tag_name)
        

    def _extract_tag(self, tag_name):
        if tag_name == 'APIC':
            tag = self.audiotags.getall('APIC')
            if tag:
                tag = tag[0].data
            else:
                tag = b''
        else:
            tag = self.audiotags.get(tag_name)
            if tag:
                tag = str(tag.text[0]) if tag_name == 'TDRC' else tag.text[0]
            else:
                tag = ''

        return tag


    def _write_tag(self, tag_name, new_value):
        match tag_name:
            case 'TPE1':
                self.audiotags.add(TPE1(encoding=3, text=new_value))
            case 'TIT2':
                self.audiotags.add(TIT2(encoding=3, text=new_value))
            case 'TALB':
                self.audiotags.add(TALB(encoding=3, text=new_value))
            case 'TCON':
                self.audiotags.add(TCON(encoding=3, text=new_value))
            case 'TDRC':
                self.audiotags.add(TDRC(encoding=3, text=new_value))
            case 'APIC':
                self.audiotags.add(APIC(encoding=3, mime='image/jpeg', type=3, desc='Cover', data=new_value))


    def update_tags_shazam(self, replace_info=True):
        shazam_out = asyncio.run(shazam_find_track_info(self.filepath))

        for tag_name in self.supported_tags:
            if replace_info or self.tags[tag_name] == '' or self.tags[tag_name] == b'':
                match tag_name:
                    case 'TPE1':
                        self.tags[tag_name] = shazam_out['track']['subtitle'].upper()
                    case 'TIT2':
                        self.tags[tag_name] = shazam_out['track']['title']
                    case 'TALB':
                        self.tags[tag_name] = shazam_out['track']['sections'][0]['metadata'][0]['text']
                    case 'TCON':
                        self.tags[tag_name] = shazam_out['track']['genres']['primary']
                    case 'TDRC':
                        self.tags[tag_name] = shazam_out['track']['sections'][0]['metadata'][2]['text']
                    case 'APIC':
                        self.tags[tag_name] = urllib.request.urlopen(shazam_out['track']['images']['coverarthq']).read()

    
    def save_as(self, new_filepath=None):
        for tag_name in self.supported_tags: 
            self._write_tag(tag_name, self.tags[tag_name])

        self.audiotags.save(self.filepath, v2_version=3)

        if not new_filepath:
            new_filepath = os.path.join(os.path.dirname(self.filepath), self.tags['TPE1'] + ' - ' + self.tags['TIT2'] + '.mp3')
        if os.path.exists(new_filepath):
            os.replace(self.filepath, new_filepath)
        else:
            os.rename(self.filepath, new_filepath)
        self.filepath = new_filepath
        