import tkinter as tk
from tkinter import filedialog as fd
from tkinter import *
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
from PIL import Image, ImageTk

import config

# set up values matrix (1,3,5,7)
max = 7
values = []
for i in range(max+1):
    if i%2!=0:
        values.append(i)
# field options
options = {'padx': 5, 'pady': 5}

class Transform:
    def __init__(self, parent,showGallery):
        self.parent = parent
        self.showGallery = showGallery;
        self.frame_main = ttk.Frame(parent.root)
        self.show_frame()
        self.UI_initialisation()
    def show_frame(self):
        self.frame_main.pack(    
            ipadx=10,
            ipady=10,
            expand=True,
            fill='both',
            side='left',
        )
    def hide_frame(self):
        self.frame_main.pack_forget()
        self.frame_main.destroy()
    
    def select_file(self):
        filetypes = (
            ('jpg files', '*.jpg'),
            ('jpeg files', '*.jpeg'),
            ('png files', '*.png'),
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        if(filename != ''):
            image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
            height, width = image.shape
            ratio = height / width
            new_width = width
            new_height = height
            if height > config.main_canvas_height or width > config.main_canvas_width:
                if ratio < 1:
                    new_width = config.main_canvas_width
                    new_height = int(new_width * ratio)
                else:
                    new_height = config.main_canvas_height
                    new_width = int(new_height * (1 / ratio))
            new_image = cv2.resize(image, (new_width, new_height))
            self.new_image= ImageTk.PhotoImage(
                Image.fromarray(new_image))
            # self.canvas.config(width=new_width, height=new_height)
            self.canvas.create_image(
                config.main_canvas_width / 2, config.main_canvas_height / 2,  image=self.new_image)
    
    def initConfigContainer(self, container):
        self.blursize_label=ttk.Label(self.config_container, text="Blur Kernel Size: ")
        self.blursize_label.grid(column=0, row=0, **options)
        self.blur_size=tk.IntVar()
        self.blursize_spinbox=ttk.Spinbox(self.config_container, from_=1, to=max, values=values, textvariable=self.blur_size)
        self.blursize_spinbox.grid(column=1, row=0, **options)

    def transform(self):
        print(self.blur_size.get())

    def UI_initialisation(self):
        self.config_frame = ttk.Frame(self.frame_main)
        self.config_frame.pack(    
            ipadx=10,
            ipady=10,
            # expand=True,
            fill='both',
            side='left',
        )
        self.btn_show = ttk.Button(self.config_frame, text="Show gallery", command=self.showGallery)
        self.btn_show.pack(
            ipadx=10,
            ipady=10,
            fill='x',
            side=TOP
        )
        self.get_img_button = ttk.Button(self.config_frame, text='Open Image', command=self.select_file)
        self.get_img_button.pack(    
            ipadx=10,
            ipady=10,
            fill='x'
        )
        self.config_container = ttk.Frame(self.config_frame)
        self.config_container.pack(    
            ipadx=10,
            ipady=10,
            fill='x'
        )
        self.canvas = Canvas(self.frame_main, bg="gray", width=config.main_canvas_width, height=config.main_canvas_height)
        self.canvas.pack(
            ipadx=10,
            ipady=10,
            expand=True,
            fill='both',
            side='right'
        )
        self.initConfigContainer(self)
        self.get_blursize_button = ttk.Button(self.config_frame, text='Transform', command=self.transform)
        self.get_blursize_button.pack(    
            ipadx=10,
            ipady=10,
            fill='x'
        )