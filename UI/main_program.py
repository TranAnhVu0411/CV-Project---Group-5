import tkinter as tk
from tkinter import *
from tkinter import ttk

import config
import image
from gallery import Gallery
from transform import Transform


class MainWindow:
    def __init__(self):
        self.root = Tk()
        self.root.geometry(str(config.window_width)+"x"+str(config.window_height))
        self.initUI()
    def showGallery(self):
        self.transform.frame_main.pack_forget()
        self.gallery.show_frame()

    def showTransform(self):
        self.gallery.frame_main.pack_forget()
        self.transform.show_frame()

    def initUI(self):
        self.gallery = Gallery(self, self.showTransform)
        self.gallery.frame_main.pack_forget()
        self.transform = Transform(self,self.showGallery)
        
image.init()
main =MainWindow()
main.root.mainloop()

