from tkinter import *
from tkinter import ttk

from gallery import Gallery


class MainWindow:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("1200x600")
        self.initUI()
    def showGallery(self):
        self.btn_show.pack_forget()
        if hasattr(self,"gallery"):
            self.gallery.show_frame()
        else:
            self.gallery = Gallery(self.root,self.hideGallery)
    def hideGallery(self):
        self.btn_show.pack(    
            ipadx=10,
            ipady=10,
            fill='x'
        )
        if hasattr(self,"gallery"):
            self.gallery.frame_main.pack_forget()
    def initUI(self):
        self.btn_show = ttk.Button(self.root, text="Show gallery", command=self.showGallery)
        self.btn_show.pack(
            ipadx=10,
            ipady=10,
            fill='x',
            side=TOP
        )


main =MainWindow()
main.root.mainloop()
