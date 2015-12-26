#!/usr/bin/env python
# -*- coding: utf-8 -*-

from eyed3.id3 import Tag, TagException
from eyed3.id3 import ID3_V1_0, ID3_V1_1, ID3_V2_3, ID3_V2_4

class ID3Tagger(object):
    def __init__(self, filepath):
        self.filepath = filepath
        self.tag = Tag()

    def parse(self):
        self.tag.parse(self.filepath)
        return self

    def save(self):
        try:
            self.tag.save(self.filepath, version=ID3_V2_4, encoding="utf8")
        except TagException:
            pass

        try:
            self.tag.save(self.filepath, version=ID3_V2_3, encoding="utf8")
        except TagException:
            pass

        # Loss of the release date month and day.
        # Loss of the comment with description.
        try:
            self.tag.save(self.filepath, version=ID3_V1_1, encoding="utf8")
        except (TagException, UnicodeEncodeError):
            pass

        # Loses what v1.1 loses, and the track #
        try:
            self.tag.save(self.filepath, version=ID3_V1_0, encoding="utf8")
        except (TagException, UnicodeEncodeError):
            pass

    def __getattr__(self, name):
        return getattr(self.tag, name)

    def __setattr__(self, name, value):
        if name in ['filepath', 'tag']:
            self.__dict__[name] = value
        else:
            setattr(self.tag, name, value)

if __name__ == '__main__':
    import sys
    import os

    SOURCE_DIR = sys.argv[1]
    TAG = "Music Pack ♫".decode('utf-8')
    for (dirpath, dirnames, filenames) in os.walk(SOURCE_DIR):
        for filename in filenames:
            tagger = ID3Tagger(os.path.join(dirpath, filename))
            tagger.parse()
            tagger.title = TAG + ' ' + tagger.title if tagger.title else TAG
            tagger.album = TAG + ' ' + tagger.album if tagger.album else TAG
            tagger.save()
