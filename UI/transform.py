import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
from PIL import Image, ImageTk
import edge_detection


import config
import gallery
import image

# set up values matrix (1,3,5,7,9,11)
max = 11
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
        self.filename=''
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

        self.filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        if(self.filename != ''):
            self.image = cv2.imread(self.filename, cv2.IMREAD_GRAYSCALE)
            height, width = self.image.shape
            ratio = height / width
            self.new_width = width
            self.new_height = height
            if height > config.main_canvas_height or width > config.main_canvas_width:
                if ratio < 1:
                    self.new_width = config.main_canvas_width
                    self.new_height = int(self.new_width * ratio)
                else:
                    self.new_height = config.main_canvas_height
                    self.new_width = int(self.new_height * (1 / ratio))
            new_image = cv2.resize(self.image, (self.new_width, self.new_height))
            self.new_image= ImageTk.PhotoImage(
                Image.fromarray(new_image))
            # self.canvas.config(width=self.new_width, height=self.new_height)
            self.canvas.create_image(
                config.main_canvas_width / 2, config.main_canvas_height / 2,  image=self.new_image)

    def initBlurConfigContainer(self):
        # Choose Blur Type
        blur_type_label=ttk.Label(self.blur_config_container, text="Blur Type: ")
        blur_type_label.grid(column=0, row=0, **options)
        self.blur_type = tk.StringVar()
        self.blur_type_combobox = ttk.Combobox(self.blur_config_container, textvariable=self.blur_type)
        self.blur_type_combobox['values'] = ["Mean filter", "Gaussian filter", "None"]
        self.blur_type_combobox['state'] = 'readonly'
        self.blur_type_combobox.current(2) # set default value == "Prewitt"
        self.blur_type_combobox.grid(column=1, row=0, **options)
        self.blur_config_frame = Frame(self.blur_config_container)
        def show_blur_config(event):
            """ handle the gradient type change event """
            if self.blur_type_combobox.get()=="None":
                self.blur_config_frame.grid_forget()
            else:
                self.blur_config_frame.grid(column=0, row=1, columnspan=2)
        self.blur_type_combobox.bind('<<ComboboxSelected>>', show_blur_config)
        
        # Set Kernel Size
        blursize_label=ttk.Label(self.blur_config_frame, text="Blur Kernel Size: ")
        blursize_label.grid(column=0, row=0, **options)
        self.blur_size=tk.IntVar()
        blursize_spinbox=ttk.Spinbox(self.blur_config_frame, from_=1, to=max, values=values, textvariable=self.blur_size, wrap=True)
        blursize_spinbox.delete(0,"end") # set default value to 1
        blursize_spinbox.insert(0,1)
        blursize_spinbox.grid(column=1, row=0, **options)

    def initEdgeDetectConfigContainer(self):
        # detection type
        self.detection_type_notebook = ttk.Notebook(self.edge_detect_config_container)
        self.detection_type_notebook.grid(column=0, row=0, columnspan=2, **options)

        # detection by threshold
        self.threshold_frame = ttk.Frame(self.detection_type_notebook)

        # skipping threshold frame
        threshold_label=ttk.Label(self.threshold_frame, text="Threshold: ")
        threshold_label.grid(column=0, row=0, **options)
        self.skipping_threshold=tk.IntVar()
        threshold_spinbox=ttk.Spinbox(self.threshold_frame, from_=1, to=255, textvariable=self.skipping_threshold, wrap=True)
        threshold_spinbox.delete(0,"end") # set default value to 1
        threshold_spinbox.insert(0,1)
        threshold_spinbox.grid(column=1, row=0, **options)

        # config gradient type
        gradient_label=ttk.Label(self.threshold_frame, text="Gradient Type: ")
        gradient_label.grid(column=0, row=1, **options)
        self.gradient_type = tk.StringVar()
        self.gradient_type_combobox = ttk.Combobox(self.threshold_frame, textvariable=self.gradient_type)
        self.gradient_type_combobox['values'] = ["Prewitt", "Sobel", "Laplacian"]
        self.gradient_type_combobox['state'] = 'readonly'
        self.gradient_type_combobox.current(0) # set default value == "prewitt"
        self.gradient_type_combobox.grid(column=1, row=1, **options)
        
        self.gradient_config_frame = ttk.Frame(self.threshold_frame)
        def show_gradient_size_config(event):
            """ handle the gradient type change event """
            if self.gradient_type_combobox.get()=="Prewitt":
                self.gradient_config_frame.grid_forget()
            else:
                self.gradient_config_frame.grid(column=0, row=2, columnspan=2)
        self.gradient_type_combobox.bind('<<ComboboxSelected>>', show_gradient_size_config)
        kernelsize_label=ttk.Label(self.gradient_config_frame, text="Kernel Size: ")
        kernelsize_label.grid(column=0, row=0, **options)
        self.gradient_size=tk.IntVar()
        kernelsize_spinbox=ttk.Spinbox(self.gradient_config_frame, from_=1, to=max, values=values, textvariable=self.gradient_size)
        kernelsize_spinbox.delete(0,"end")
        kernelsize_spinbox.insert(0,1)
        kernelsize_spinbox.grid(column=1, row=0, **options)
        self.detection_type_notebook.add(self.threshold_frame, text='Skipping Threshold')

        # detection by canny
        canny_frame = ttk.Frame(self.detection_type_notebook)

        # config max threshold (V2)
        max_threshold_label=ttk.Label(canny_frame, text="Max Threshold: ")
        max_threshold_label.grid(column=0, row=0, **options)
        self.max_threshold=tk.IntVar()
        max_threshold_spinbox=ttk.Spinbox(canny_frame, from_=1, to=255, textvariable=self.max_threshold, wrap=True)
        max_threshold_spinbox.delete(0,"end") # set default value to 200
        max_threshold_spinbox.insert(0,200)
        max_threshold_spinbox.grid(column=1, row=0, **options)

        # config min threshold (V1)
        min_threshold_label=ttk.Label(canny_frame, text="Min Threshold: ")
        min_threshold_label.grid(column=0, row=1, **options)
        self.min_threshold=tk.IntVar()
        min_threshold_spinbox=ttk.Spinbox(canny_frame, from_=1, to=255, textvariable=self.min_threshold, wrap=True)
        min_threshold_spinbox.delete(0,"end") # set default value to 100
        min_threshold_spinbox.insert(0,100)
        min_threshold_spinbox.grid(column=1, row=1, **options)

        self.detection_type_notebook.add(canny_frame, text='Canny')
    
    def get_param(self):
        blur_type = self.blur_type.get()
        blur_ksize = self.blur_size.get()
        
        use_edge_detection=self.use_edge_detection.get()
        if self.use_edge_detection.get()=="":
            use_edge_detection="no"
        edge_detection_type = self.detection_type_notebook.tab(self.detection_type_notebook.select(), "text")
        
        gradient_type = self.gradient_type.get()
        gradient_size = self.gradient_size.get()
        skipping_threshold = self.skipping_threshold.get()

        min_threshold = self.min_threshold.get()
        max_threshold = self.max_threshold.get()
        return (blur_type, blur_ksize, 
                use_edge_detection, edge_detection_type,
                gradient_type, gradient_size, skipping_threshold,
                max_threshold, min_threshold)

    def transform(self):
        if self.filename=="":
            messagebox.showwarning("Warning", "You haven't open any image")
        else:
            self.transform_image = edge_detection.edge_detection(self.image, *self.get_param())
            
            new_transform_image = cv2.resize(self.transform_image, (self.new_width, self.new_height))
            self.new_transform_image= ImageTk.PhotoImage(Image.fromarray(new_transform_image))
            # self.canvas.config(width=self.new_width, height=self.new_height)
            self.canvas.create_image(
                config.main_canvas_width / 2, config.main_canvas_height / 2,  image=self.new_transform_image)
    
    def save(self):
        if self.filename=="":
            messagebox.showwarning("Warning", "You haven't open any image")
        else:
            self.transform_image = edge_detection.edge_detection(self.image, *self.get_param())
            image_obj = image.image_object(self.transform_image, *self.get_param())
            gallery.list_image.append(image_obj)            

    def UI_initialisation(self):
        self.frame_main.columnconfigure(0, weight=1)
        self.frame_main.columnconfigure(1, weight=1)
        self.config_frame = Frame(self.frame_main)
        self.config_frame.grid(column=0, row=0)
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
        self.blur_config_container = ttk.LabelFrame(self.config_frame, text="Blur Config")
        self.blur_config_container.pack(    
            ipadx=10,
            ipady=10,
            fill='x'
        )
        self.initBlurConfigContainer()

        self.edge_detect_config_container = ttk.Frame(self.config_frame)

        self.use_edge_detection = tk.StringVar()
        def show_edge_detect_config():
            if self.use_edge_detection.get() == 'yes':
                self.edge_detect_config_container.pack(ipadx=10,
                                             ipady=10,
                                             fill='x')
            else:
                self.edge_detect_config_container.pack_forget()

        ttk.Checkbutton(self.config_frame,
                        text='Sử dụng Edge Detection?',
                        command=show_edge_detect_config,
                        variable=self.use_edge_detection,
                        onvalue='yes',
                        offvalue='no').pack(ipadx=10,
                                                  ipady=10,
                                                  fill='x')
                    
        self.initEdgeDetectConfigContainer()
        
        self.transform_button = ttk.Button(self.config_frame, text='Transform', command=self.transform)
        self.transform_button.pack(    
            ipadx=10,
            ipady=10,
            fill='x',
            side=BOTTOM
        )

        self.save_button = ttk.Button(self.config_frame, text='Save Image to Gallery', command=self.save)
        self.save_button.pack(    
            ipadx=10,
            ipady=10,
            fill='x',
            side=BOTTOM
        )

        self.canvas = Canvas(self.frame_main, bg="gray", width=config.main_canvas_width, height=config.main_canvas_height)
        self.canvas.grid(column=1, row=0)