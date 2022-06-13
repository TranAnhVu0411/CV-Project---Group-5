from tkinter import *
from tkinter import ttk

import cv2
import numpy as np
from PIL import Image, ImageTk

import config


class Gallery:
    def __init__(self, parent,showTransform):
        self.showTransform = showTransform;
        self.frame_main = ttk.Frame(parent.root, width=config.window_width, height=config.window_height)
        self.show_frame()
        self.getListImg()
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
    def getListImg(self): #actually get from parents
        list_image_path = [
        "./sample_image/bear_cat.jpeg",
        "./sample_image/cat.jpeg",
        "./sample_image/dumpling_cat.jpeg",
        "./sample_image/gamatoto.jpeg",
        "./sample_image/hula_cat.jpeg",
        "./sample_image/ototo.jpeg",
        "./sample_image/puppet_cat.jpeg",
        "./sample_image/rice_cat.jpeg",
        "./sample_image/robo_cat.jpeg"
        ]
        self.list_image = []
        self.list_thumb = []
        for path in list_image_path:
            tmp =Image.open(path) 
            self.list_image.append(tmp) 
            thumb = tmp.copy()
            thumb.thumbnail((config.images_scroll_height-20, config.images_scroll_height-20))
            python_image = ImageTk.PhotoImage(thumb)
            self.list_thumb.append(python_image)
    def UI_initialisation(self):
        #menu info
        self.frame_info = ttk.Frame(self.frame_main)
        self.frame_info.pack(    
            ipadx=10,
            ipady=10,
            padx=30,
            # expand=True,
            fill='both',
            side='left',
        )
        # self.frame_info.grid(row=0, column=0, columnspan=10,  padx=5, pady=5)
        ttk.Button(
        self.frame_info, text="Back", command=self.showTransform).pack(    
            ipadx=10,
            ipady=10,
            fill='x'
        )

        # ttk.Button(
        # self.frame_info, text="Back", command=self.hide_frame).grid(row=0, column=0)

        self.label_title = Label( self.frame_info, text ="Hey!? How are you doing?" , width=35)
        self.label_title.pack(    
            ipadx=10,
            ipady=10,
            fill='x'
        )
        self.var_name = StringVar("")

        self.label_name = Label( self.frame_info, textvariable =self.var_name,wraplength=150, justify="center" )
        self.label_name.pack(    
            ipadx=10,
            ipady=10,
            padx=30,
            fill='x'
        )
        self.var_name.set("filename")


        # Create A Gallery

        self.gallery_frame_container = Frame(self.frame_main)

        self.gallery_frame_container.pack(
            ipadx=10,
            ipady=10,
            padx=(200,0),
            expand=True,
            fill='both',
            side='right'
        )
        # self.gallery_frame_container.grid(row=0, column=10,rowspan=20, columnspan=15,  padx=5, pady=5)

        # Create Frame for X Scrollbar
        self.sec = Frame(self.gallery_frame_container)
        self.sec.pack(fill=X,side=BOTTOM)


        # Create A Canvas scroll

        self.canvas_scroll = Canvas(self.gallery_frame_container)
        self.canvas_scroll.pack(side=LEFT,fill=BOTH,expand=True)


        # Add A Scrollbars to Canvas

        x_scrollbar = ttk.Scrollbar(self.sec,orient=HORIZONTAL,command=self.canvas_scroll.xview)
        x_scrollbar.pack(side=BOTTOM,fill=X)

        y_scrollbar = ttk.Scrollbar(self.gallery_frame_container,orient=VERTICAL,command=self.canvas_scroll.yview)
        y_scrollbar.pack(side=RIGHT,fill=Y)

        # Configure the canvas

        self.canvas_scroll.configure(xscrollcommand=x_scrollbar.set)
        self.canvas_scroll.configure(yscrollcommand=y_scrollbar.set)
        self.canvas_scroll.bind("<Configure>",lambda e: self.canvas_scroll.config(scrollregion= self.canvas_scroll.bbox(ALL))) 


        # Create Another Frame INSIDE the Canvas
        self.frame_scroll = ttk.Frame(self.canvas_scroll)
        self.frame_scroll.pack()
        # self.frame_scroll.config(relief=RIDGE, padding=(50, 15))

        #menu
        self.gallery_frame = ttk.Frame(self.frame_scroll)
        self.gallery_frame.pack()
        # self.gallery_frame.config(relief=RIDGE, padding=(50, 15))

        self.canvas_img_show = Canvas(self.gallery_frame, bg="gray", width=config.canvas_width, height=config.canvas_height)
        self.canvas_img_show.grid(row=0, column=0, columnspan=10, rowspan=10)
        Button(
            self.gallery_frame, text="Remove").grid(
            row=5, column=10, columnspan=2,  padx=5, pady=5, sticky='sw')
        Button(
            self.gallery_frame, text="Save").grid(
            row=6, column=10, columnspan=2,  padx=5, pady=5, sticky='sw')
        Button(
            self.gallery_frame, text="Save all").grid(
            row=9, column=10, columnspan=2, padx=5, pady=5, sticky='sw')

        self.canvas_scroll_thumb = Canvas(self.gallery_frame, width=config.images_scroll_width, height=config.images_scroll_height)
        self.canvas_scroll_thumb.grid(row=10, column=3)
        # self.canvas_scroll_thumb.pack(side=LEFT,fill=BOTH,expand=1)

        self.frame_thumb = Frame(self.canvas_scroll_thumb)
        self.frame_thumb.pack()

        x_scrollbar_thumb = ttk.Scrollbar(self.frame_scroll,orient=HORIZONTAL,command=self.canvas_scroll_thumb.xview)
        x_scrollbar_thumb.pack(side=BOTTOM,fill=X)

        self.canvas_scroll_thumb.configure(xscrollcommand=x_scrollbar_thumb.set)
        self.canvas_scroll_thumb.bind("<Configure>",lambda e: self.canvas_scroll_thumb.config(scrollregion= self.canvas_scroll_thumb.bbox(ALL))) 

        #setup list thumbnail button
        self.list_btn = []
        for ind, image in enumerate(self.list_image):
            print(image.filename)
            button = Button(self.frame_thumb, image=self.list_thumb[ind])
            button.grid(row=5,column=ind,pady=10,padx=10)
            self.list_btn.append(button)
            button.configure(command= lambda ind=ind: self.clickHandle(ind) )

        self.canvas_scroll_thumb.create_window((0,0),window= self.frame_thumb, anchor="nw")

        # Add that New Frame a Window In The Canvas
        self.canvas_scroll.create_window((0,0),window= self.frame_scroll, anchor="nw")


    def display_image(self,image=None):
        self.canvas_img_show.delete("all")
        image =  np.array(image) #cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB)
        height, width, channels = image.shape
        ratio = height / width
        new_width = width
        new_height = height
        if height > config.canvas_height or width > config.canvas_width:
            if ratio < 1:
                new_width = config.canvas_width
                new_height = int(new_width * ratio)
            else:
                new_height = config.canvas_height
                new_width = int(new_height * (width / height))
        new_image = cv2.resize(image, (new_width, new_height))
        self.new_image= ImageTk.PhotoImage(
            Image.fromarray(new_image))

        self.canvas_img_show.config(width=new_width, height=new_height)
        self.canvas_img_show.create_image(
            new_width / 2, new_height / 2,  image=self.new_image)
    
    def clickHandle(self,ind):
        print(ind)
        for btn in self.list_btn:
            btn.configure(state = NORMAL)
        self.list_btn[ind].configure(state =DISABLED)
        self.var_name.set(self.list_image[ind].filename)
        self.display_image(self.list_image[ind])
