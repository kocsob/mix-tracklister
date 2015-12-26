#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Balazs Kocso"
__version__ = "1.1"

OS_DATE_FORMAT = "%Y.%m.%d"
DATE_FORMAT = "%Y.%m.%d."

import os
import shutil

from Tkinter import *
from tkFileDialog import askopenfilename, askdirectory
import dateparser

from id3_tagger import ID3Tagger

class Tracklister(object):
    def make_tracklist(self):
        artist = unicode(self.artist_entry.get().strip())
        title = unicode(self.title_entry.get().strip())
        date = dateparser.parse(self.date_entry.get().strip())
        tracklist = unicode(self.tracklist_textbox.get("0.0", END).strip())
        original_file = unicode(self.filepath_entry.get().strip())
        target_dir = unicode(self.dirpath_entry.get().strip())

        # Prepare strings for os name
        prepared_artist = self.prepare_string(artist)
        prepared_title = self.prepare_string(title)
        os_name = date.strftime(OS_DATE_FORMAT) + "_" + prepared_artist + "_-_" + prepared_title

        if tracklist:       # Create new folder and make tracklist file
            new_dir = os.path.join(target_dir, os_name)
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)
            target_dir = new_dir

            self.make_tracklist_file(
                filepath=os.path.join(target_dir, os_name + '.txt'),
                artist=artist,
                title=title,
                date=date,
                tracklist=tracklist
            )

        # Move file
        destination = os.path.join(target_dir, os_name + ".mp3")
        shutil.move(original_file, destination)

        # Make ID3 Tag
        self.make_ID3_tag(destination, artist, title, date)

        # Finish
        print(artist + " - " + title + " finished!!!")

    @classmethod
    def prepare_string(cls, text):
        # Whitespaces
        text = text.strip()
        text = text.replace(u' ', u'_')

        # Small characters
        text = text.replace(u'á', u'a')
        text = text.replace(u'é', u'e')
        text = text.replace(u'í', u'i')
        text = text.replace(u'ó', u'o')
        text = text.replace(u'ö', u'o')
        text = text.replace(u'ő', u'o')
        text = text.replace(u'ú', u'u')
        text = text.replace(u'ü', u'u')
        text = text.replace(u'ű', u'u')

        # Big characters
        text = text.replace(u'Á', u'A')
        text = text.replace(u'É', u'E')
        text = text.replace(u'Í', u'I')
        text = text.replace(u'Ó', u'O')
        text = text.replace(u'Ö', u'O')
        text = text.replace(u'Ő', u'O')
        text = text.replace(u'Ú', u'U')
        text = text.replace(u'Ü', u'U')
        text = text.replace(u'Ű', u'U')

        return text

    @classmethod
    def make_ID3_tag(cls, filepath, artist, title, date):
        tagger = ID3Tagger(filepath)
        tagger.artist = artist
        tagger.title = title + " " + date.strftime(DATE_FORMAT)
        tagger.genre = u"House"
        tagger.track_num = 1
        tagger.recording_date = date.year
        tagger.save()

    @classmethod
    def make_tracklist_file(cls, filepath, artist, title, date, tracklist):
        with open(filepath, "w") as tracklist_file:
            tracklist_file.write((artist + u" - " + title + u" " + date.strftime(DATE_FORMAT)).encode("utf-8"))
            for i in range(5):
                tracklist_file.write("\n")
            tracklist_file.write("Tracklist:")
            for i in range(5):
                tracklist_file.write("\n")
            tracklist_file.write((tracklist).encode("utf-8"))

    def __init__(self):
        self.window = Tk()
        self.window.title("Mix tracklister")

        # Choose file
        choose_file_label = Label(self.window, text='Choose file:', anchor=W)
        choose_file_label.pack(fill=X)
        choose_file_frame = Frame(self.window)
        self.filepath_entry = Entry(choose_file_frame, width=100)
        self.filepath_entry.pack(side=LEFT)
        file_browser_button = Button(choose_file_frame, text='Browse', command=self.choose_file_event_handler)
        file_browser_button.pack(side=LEFT)
        choose_file_frame.pack(fill=X, expand=YES)

        # Choose directory
        choose_dir_label = Label(self.window, text='Choose directory:', anchor=W)
        choose_dir_label.pack(fill=X)
        choose_dir_frame = Frame(self.window)
        self.dirpath_entry = Entry(choose_dir_frame, width=100)
        self.dirpath_entry.pack(side=LEFT)
        dir_browser_button = Button(choose_dir_frame, text='Browse', command=self.choose_directory_event_handler)
        dir_browser_button.pack(side=LEFT)
        choose_dir_frame.pack(fill=X, expand=YES)

        # Artist
        artist_label = Label(self.window, text='Artist:', anchor=W)
        artist_label.pack(fill=X)
        self.artist_entry = Entry(self.window)
        self.artist_entry.pack(fill=X)

        # Title
        title_label = Label(self.window, text='Title:', anchor=W)
        title_label.pack(fill=X)
        self.title_entry = Entry(self.window)
        self.title_entry.pack(fill=X)

        # Date
        date_label = Label(self.window, text='Date:', anchor=W)
        date_label.pack(fill=X)
        self.date_entry = Entry(self.window)
        self.date_entry.pack(fill=X)

        # Tracklist
        tracklist_label = Label(self.window, text='Tracklist:', anchor=W)
        tracklist_label.pack(fill=X)
        self.tracklist_textbox = Text(self.window)
        self.tracklist_textbox.pack()

        # Add short key bindings to the text box
        self.tracklist_textbox.bind("<Control-Key-a>", self.select_all_event_handler)
        self.tracklist_textbox.bind("<Control-Key-A>", self.select_all_event_handler) # just in case caps lock is on

        # Make tracklist Button
        make_tracklist_button = Button(self.window, text='Make tracklist', command=self.make_tracklist, width=20)
        make_tracklist_button.pack()

        #Separator
        separator = Frame(height=2, bd=1, relief=SUNKEN)
        separator.pack(fill=X, padx=5, pady=10)

        #Exit Button
        exit_button = Button(self.window, text='Exit', command=self.window.destroy, width=20)
        exit_button.pack()

    def choose_file_event_handler(self):
        filepath = askopenfilename(
            initialdir = unicode(self.filepath_entry.get()),
            filetypes=[('MP3 file','*.mp3'), ('All files','.*')],
            parent=self.window
        )
        if (filepath != ""):
            self.filepath_entry.delete(0, END)
            self.filepath_entry.insert(0, filepath)

    def choose_directory_event_handler(self):
        directory = askdirectory(initialdir = unicode(self.dirpath_entry.get()))
        if (directory != ""):
            self.dirpath_entry.delete(0, END)
            self.dirpath_entry.insert(0, directory)

    def select_all_event_handler(self, event):
        self.tracklist_textbox.tag_add(SEL, "0.0", END)
        self.tracklist_textbox.mark_set(INSERT, "0.0")
        self.tracklist_textbox.see(INSERT)
        return 'break'

    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    tracklister = Tracklister()
    tracklister.run()