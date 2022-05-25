import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror

# root window
root = tk.Tk()
root.title('Edge detection')
root.geometry('1000x70')
# root.resizable(False, False)


# frame
result_frame = ttk.Frame(root)
config_frame = ttk.Frame(root)


# field options
options = {'padx': 5, 'pady': 5}

# set up values matrix (1,3,5,7)
max = 7
values = []
for i in range(max+1):
    if i%2!=0:
        values.append(i)

# config blur kernel size
blursize_label=ttk.Label(config_frame, text="Blur Kernel Size: ")
blursize_label.grid(column=0, row=0, **options)
blur_size=tk.IntVar()
blursize_spinbox=ttk.Spinbox(config_frame, from_=1, to=max, values=values, textvariable=blur_size)
blursize_spinbox.grid(column=1, row=0, **options)

# detection type
detection_type_notebook = ttk.Notebook(config_frame)
detection_type_notebook.grid(column=0, row=1, columnspan=2, **options)

# detection by threshold
threshold_frame = ttk.Frame(detection_type_notebook)

# config skipping threshold
threshold_label=ttk.Label(threshold_frame, text="Threshold: ")
threshold_label.grid(column=0, row=0, **options)
threshold=tk.IntVar()
threshold_spinbox=ttk.Spinbox(threshold_frame, from_=1, to=255, textvariable=threshold, wrap=True)
threshold_spinbox.delete(0,"end") # set default value to 1
threshold_spinbox.insert(0,1)
threshold_spinbox.grid(column=1, row=0, **options)

# config gradient type
gradient_label=ttk.Label(threshold_frame, text="Gradient Type: ")
gradient_label.grid(column=0, row=1, **options)
gradient_type = tk.StringVar()
gradient_type_combobox = ttk.Combobox(threshold_frame, textvariable=gradient_type)
gradient_type_combobox['values'] = ["Prewitt", "Sobel", "Laplacian"]
gradient_type_combobox['state'] = 'readonly'
gradient_type_combobox.current(0) # set default value == "Prewitt"
gradient_type_combobox.grid(column=1, row=1, **options)

# if gradient type == "Sobel"/"Laplacian", 
# show gradient kernel size config, else, show none
def show_gradient_size_config(event):
    """ handle the gradient type change event """
    if gradient_type_combobox.get()=="Prewitt":
        gradient_config_frame.pack_forget()
    else:
        gradient_config_frame.pack()
gradient_type_combobox.bind('<<ComboboxSelected>>', show_gradient_size_config)

boundary_frame = ttk.Frame(threshold_frame)
boundary_frame.grid(column=0, row=2, **options, columnspan=2)
gradient_config_frame = ttk.LabelFrame(boundary_frame, text='Gradient Kernel Size Config')
# gradient_config_frame.pack(boundary_frame)
kernelsize_label=ttk.Label(gradient_config_frame, text="Kernel Size: ")
kernelsize_label.grid(column=0, row=0, **options)
size=tk.IntVar()
kernelsize_spinbox=ttk.Spinbox(gradient_config_frame, from_=1, to=max, values=values, textvariable=size)
kernelsize_spinbox.delete(0,"end")
kernelsize_spinbox.insert(0,1)
kernelsize_spinbox.grid(column=1, row=0, **options)

detection_type_notebook.add(threshold_frame, text='Threshold')

# detection by canny
canny_frame = ttk.Frame(detection_type_notebook)

# config max threshold (V2)
max_threshold_label=ttk.Label(canny_frame, text="Max Threshold: ")
max_threshold_label.grid(column=0, row=0, **options)
max_threshold=tk.IntVar()
max_threshold_spinbox=ttk.Spinbox(canny_frame, from_=1, to=255, textvariable=max_threshold, wrap=True)
max_threshold_spinbox.delete(0,"end") # set default value to 200
max_threshold_spinbox.insert(0,200)
max_threshold_spinbox.grid(column=1, row=0, **options)

# config min threshold (V1)
min_threshold_label=ttk.Label(canny_frame, text="Min Threshold: ")
min_threshold_label.grid(column=0, row=1, **options)
min_threshold=tk.IntVar()
min_threshold_spinbox=ttk.Spinbox(canny_frame, from_=1, to=255, textvariable=min_threshold, wrap=True)
min_threshold_spinbox.delete(0,"end") # set default value to 100
min_threshold_spinbox.insert(0,100)
min_threshold_spinbox.grid(column=1, row=1, **options)

detection_type_notebook.add(canny_frame, text='Canny')


# # convert button


# def convert_button_clicked():
#     """  Handle convert button click event 
#     """
#     try:
#         f = float(temperature.get())
#         c = fahrenheit_to_celsius(f)
#         result = f'{f} Fahrenheit = {c:.2f} Celsius'
#         result_label.config(text=result)
#     except ValueError as error:
#         showerror(title='Error', message=error)


# convert_button = ttk.Button(frame, text='Convert')
# convert_button.grid(column=2, row=0, sticky='W', **options)
# convert_button.configure(command=convert_button_clicked)

# # result label
# result_label = ttk.Label(frame)
# result_label.grid(row=1, columnspan=3, **options)

# add padding to the frame and show it
result_frame.grid(column=0, row=0, **options)
config_frame.grid(column=1, row=0, **options)


# start the app
root.mainloop()