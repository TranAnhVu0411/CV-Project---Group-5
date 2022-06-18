import os
from tkinter import *
from tkinter import messagebox, ttk
from tkinter.filedialog import askdirectory, asksaveasfile

import cv2
import numpy as np
from PIL import Image, ImageTk

import config
import image


class Gallery:
    def __init__(self, parent,showTransform):
        self.showTransform = showTransform;
        self.parent = parent
        self.frame_main = ttk.Frame(parent.root, width=config.window_width, height=config.window_height)
        self.UI_initialisation()
        self.list_btn = []
        self.show_frame()
    def show_frame(self):
        self.getListImg(image.list_image_obj)
        #setup list thumbnail button
        self.thumbnail_init()
        self.frame_main.pack(        
            ipadx=10,
            ipady=10,
            expand=True,
            fill='both',
            side='left',
        )
        

    def hide_frame(self):
        self.frame_main.pack_forget()

    def getListImg(self, list_image_object): #actually get from parents
        self.list_img_obj=[]
        self.list_image = []
        self.list_thumb = []
        for obj in list_image_object:
            self.list_img_obj.append(obj)
            tmp =Image.fromarray(obj.img) 
            self.list_image.append(tmp) 
            thumb = tmp.copy()
            thumb.thumbnail((config.images_scroll_height-20, config.images_scroll_height-20))
            python_image = ImageTk.PhotoImage(thumb)
            self.list_thumb.append(python_image)
        print(self.list_image)

    def UI_initialisation(self):
        #menu info
        self.frame_info = ttk.Frame(self.frame_main)
        self.frame_info.pack(    
            ipadx=10,
            ipady=10,
            padx=(75,0),
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
            padx=(75,0),
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
            self.gallery_frame, text="Remove", command = self.delete).grid(
            row=5, column=10, columnspan=2,  padx=5, pady=5, sticky='sw')
        Button(
            self.gallery_frame, text="Save", command = self.save).grid(
            row=6, column=10, columnspan=2,  padx=5, pady=5, sticky='sw')
        Button(
            self.gallery_frame, text="Save all", command = self.save_all).grid(
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


        self.canvas_scroll_thumb.create_window((0,0),window= self.frame_thumb, anchor="nw")

        # Add that New Frame a Window In The Canvas
        self.canvas_scroll.create_window((0,0),window= self.frame_scroll, anchor="nw")
    
    def thumbnail_init(self):
        #setup list thumbnail button
        if len(self.list_btn)!=0:
            for btn in self.list_btn:
                btn.destroy()
        self.list_btn = []
        for ind, image in enumerate(self.list_image):
            button = Button(self.frame_thumb, image=self.list_thumb[ind])
            button.grid(row=5,column=ind,pady=10,padx=10)
            self.list_btn.append(button)
            button.configure(command= lambda ind=ind: self.clickHandle(ind) )

    def display_image(self,image=None):
        self.canvas_img_show.delete("all")
        image =  np.array(image) #cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB)
        height, width = image.shape
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

        # self.canvas_img_show.config(width=new_width, height=new_height)
        self.canvas_img_show.create_image(config.canvas_width / 2, config.canvas_height / 2,  image=self.new_image)
    
    def clickHandle(self,ind):
        self.ind = ind
        for btn in self.list_btn:
            btn.configure(state = NORMAL)
        self.list_btn[ind].configure(state =DISABLED)
        self.var_name.set(self.list_img_obj[ind].show_info())
        self.display_image(self.list_image[ind])
    
    def delete(self):
        if self.ind is None:
            return
        del image.list_image_obj[self.ind]
        del self.list_image[self.ind]
        del self.list_thumb[self.ind]
        self.var_name.set("filename")
        self.ind = None
        self.thumbnail_init()
        self.canvas_img_show.delete("all")
    
    def save(self):
        if self.ind is None:
            return
        data = [('jpg files', '*.jpg'),
                ('jpeg files', '*.jpeg'),
                ('png files', '*.png'),]
        file = asksaveasfile(filetypes = data, defaultextension = data)
        print(file)
        self.list_image[self.ind].save(file.name)
    def save_all(self):
        if len(self.list_image) <= 0:
            messagebox.showerror("empty list!")
            return
        save_path = askdirectory()
        for img_obj in image.list_image_obj:
            file_name = img_obj.show_info().replace(":","_").replace(" ","").replace("\n","-")+".jpg"
            print(file_name)
            cv2.imwrite(os.path.join(save_path,file_name),img_obj.img)
        messagebox.showinfo("save successfully")
