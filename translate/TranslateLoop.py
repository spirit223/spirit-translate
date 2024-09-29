from threading import Thread

from gi.repository import GLib, Gtk, Notify

class TranslateLoop:
    def __init__(self):
        self.thread = Thread(target=Gtk.main)
        self.thread.start()