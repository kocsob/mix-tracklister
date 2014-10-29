#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Balazs Kocso"
__version__ = "1.0"

#Window building
from Tkinter import *
from tkFileDialog import askopenfilename, askdirectory

#ID3 Tags
from eyed3.id3 import Tag
from eyed3.id3 import ID3_V1_0, ID3_V1_1, ID3_V2_3, ID3_V2_4

#import logging
#from eyed3 import log
#log.setLevel(logging.DEBUG)

#OS
import os
import shutil #For file move


directory = ""
filepath = ""


def MakeID3Tag(file, artist, title, date):
    t = Tag()
    t.artist = artist
    t.title = title + " " + date
    t.genre = u"House"
    t.track_num = 1
    t.recording_date = date[:4]

    t.save(file, version=ID3_V2_4)
    t.save(file, version=ID3_V2_3)

    # Loss of the release date month and day.
    # Loss of the comment with description.
    t.save(file, version=ID3_V1_1)

    # Loses what v1.1 loses, and the track #
    t.save(file, version=ID3_V1_0)

def PrepareString(text):
    #White spaces
    trim = text.strip()
    text = text.replace(u' ', u'_')

    #small chars
    text = text.replace(u'á', u'a')
    text = text.replace(u'é', u'e')
    text = text.replace(u'í', u'i')
    text = text.replace(u'ó', u'o')
    text = text.replace(u'ö', u'o')
    text = text.replace(u'ő', u'o')
    text = text.replace(u'ú', u'u')
    text = text.replace(u'ü', u'u')
    text = text.replace(u'ű', u'u')
    
    #Big chars
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

def DoIt():
    artist = unicode(artist_entry.get())
    title = unicode(title_entry.get())
    date = unicode(date_entry.get())
    tracklist = unicode(tracklist_textbox.get("0.0",END))
    
    filepath = unicode(filepath_entry.get())
    directory = unicode(dirpath_entry.get())
    
    #Create directory
    preparedartist = PrepareString(artist)
    preparedtitle = PrepareString(title)
    newdir = os.path.join(directory, date[:10] + "_" + preparedartist + "_-_" + preparedtitle)
    if not os.path.exists(newdir):
        os.makedirs(newdir)
    
    #Create tracklist file
    tl_file = file(os.path.join(newdir, preparedartist + "_-_" + preparedtitle + "_" + date[:-1] + ".txt"), "w")
    tl_file.write((artist + u" - " + title + u" " + date).encode("utf-8"))
    for i in range(5):
        tl_file.write("\n")
    tl_file.write("Tracklist:")
    for i in range(5):
        tl_file.write("\n")
    tl_file.write((tracklist).encode("utf-8"))
    tl_file.close()
    
    #Move file
    destination = os.path.join(newdir, preparedartist + "_-_" + preparedtitle + "_" + date[:-1] + ".mp3")
    shutil.move(filepath, destination)
    
    #Make ID3 Tag
    MakeID3Tag(destination, artist, title, date)
    
    #Finish
    print(artist + " - " + title + " finished!!!")
    

def ChooseFile():
    filepath = askopenfilename(initialdir = unicode(filepath_entry.get()))
    if (filepath != ""):
        filepath_entry.delete(0, END)
        filepath_entry.insert(0, filepath)


def ChooseDir():
    directory = askdirectory(initialdir = unicode(dirpath_entry.get()))
    if (directory != ""):
        dirpath_entry.delete(0, END)
        dirpath_entry.insert(0, directory)


# Select all the text in textbox (not working)
def select_all(event):
    tracklist_textbox.tag_add(SEL, "1.0", END)
    tracklist_textbox.mark_set(INSERT, "1.0")
    tracklist_textbox.see(INSERT)
    return 'break'


#MAIN
window = Tk()
window.wm_title("Tracklister")


#Choose file
choosefile_label = Label(window, text='Choose file:', anchor="w")
choosefile_label.pack(fill="x")
choosefile_frame = Frame(window)
filepath_entry = Entry(choosefile_frame, width="100")
filepath_entry.pack(side="left")
filebrowse_button = Button(choosefile_frame, text='Browse', command=ChooseFile)
filebrowse_button.pack(side="left")
choosefile_frame.pack(fill="x", expand="yes")

#Choose directory
choosedir_label = Label(window, text='Choose directory:', anchor="w")
choosedir_label.pack(fill="x")
choosedir_frame = Frame(window)
dirpath_entry = Entry(choosedir_frame, width="100")
dirpath_entry.pack(side="left")
dirbrowse_button = Button(choosedir_frame, text='Browse', command=ChooseDir)
dirbrowse_button.pack(side="left")
choosedir_frame.pack(fill="x", expand="yes")

#Artist
artist_label = Label(window, text='Artist:', anchor="w")
artist_label.pack(fill="x")
artist_entry = Entry(window)
artist_entry.pack(fill="x")

#Title
title_label = Label(window, text='Title:', anchor="w")
title_label.pack(fill="x")
title_entry = Entry(window)
title_entry.pack(fill="x")

#Date
date_label = Label(window, text='Date:', anchor="w")
date_label.pack(fill="x")
date_entry = Entry(window)
date_entry.pack(fill="x")

#Tracklist:
tracklist_label = Label(window, text='Tracklist:', anchor="w")
tracklist_label.pack(fill="x")
tracklist_textbox = Text(window)
tracklist_textbox.pack()
# Add the binding
tracklist_textbox.bind("<Control-Key-a>", select_all)
tracklist_textbox.bind("<Control-Key-A>", select_all) # just in case caps lock is on

#Do It Button
doit_button = Button(window, text='Do It', command=DoIt, width="20")
doit_button.pack()

#Separator
separator = Frame(height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=5, pady=10)

#Exit Button
exit_button = Button(window, text='Exit', command = window.destroy, width="20")
exit_button.pack()

#Window
window.mainloop()