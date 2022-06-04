from tkinter import *
from tkinter import ttk

import cv2
import numpy as np
from PIL import Image, ImageTk


class Gallery:
    def __init__(self, master, call_back_hide):
        self.frame_main = ttk.Frame(master)
        self.hide_frame = call_back_hide
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
    def getListImg(self): #actually get from parents
        list_image_path = [
        "../logo2.png",
        "D:/BG/5k-2560x1440-4k-wallpaper-forest-osx-apple-lake-water-yosemite-169.jpg",
        "D:/BG/a_little_windy_by_shootingstarlogbook_deu36jc-fullview.jpg",
        "D:/BG/abstract-nature-1920x1080-8k-21456-1536x864.jpg",
        "D:/BG/aloe-2560x1440-green-4k-23513.jpg",
        "D:/BG/alps-2560x1440-switzerland-mountains-clouds-5k-16936.jpg",
        "D:/BG/antarctica-2560x1440-5k-4k-wallpaper-iceberg-blue-water-ocean-sea-1160.jpg",
        "D:/BG/antarctica-2560x1440-iceberg-ocean-4k-16235.jpg",
        "D:/BG/antarctica-2560x1440-iceberg-ocean-5k-16236.jpg"
        ]
        self.list_image = []
        self.list_thumb = []
        for path in list_image_path:
            tmp =Image.open(path) 
            self.list_image.append(tmp) 
            thumb = tmp.copy()
            thumb.thumbnail((150,150))
            python_image = ImageTk.PhotoImage(thumb)
            self.list_thumb.append(python_image)
    def UI_initialisation(self):
        #menu info
        self.frame_info = ttk.Frame(self.frame_main)
        self.frame_info.pack(    
            ipadx=10,
            ipady=10,
            expand=True,
            fill='both',
            side='left',
        )
        # self.frame_info.grid(row=0, column=0, columnspan=10,  padx=5, pady=5)
        ttk.Button(
        self.frame_info, text="Back", command=self.hide_frame).pack(    
            ipadx=10,
            ipady=10,
            fill='x'
        )

        self.label_title = Label( self.frame_info, text ="Hey!? How are you doing?" )
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
            fill='x'
        )
        self.var_name.set("filename")


        # Create A Gallery

        self.gallery_frame_container = Frame(self.frame_main)

        self.gallery_frame_container.pack(
            ipadx=10,
            ipady=10,
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
        self.canvas_scroll.pack(side=BOTTOM,fill=BOTH,expand=1)


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
        # self.frame_menu.config(relief=RIDGE, padding=(50, 15))

        self.canvas_img_show = Canvas(self.gallery_frame, bg="gray", width=600, height=450)
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

        self.canvas_scroll_thumb = Canvas(self.gallery_frame, width=600, height=150)
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
        if height > 480 or width > 600:
            if ratio < 1:
                new_width = 600
                new_height = int(new_width * ratio)
            else:
                new_height = 480
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
