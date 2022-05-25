import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image



root = tk.Tk()
root.title('Pack Demo')
root.geometry("930x1000")
# root.columnconfigure(0, weight=1)
# root.columnconfigure(1, weight=3)

photo = ImageTk.PhotoImage(Image.open('/Users/trananhvu/Documents/CV/RGB_001.jpeg').resize((450, 350), Image.ANTIALIAS))
originalImage = ttk.Label(
    root,
    image=photo,
    text='Original',
    compound='top'
)
originalImage.grid(column=0, row=1, padx=5, pady=5)

transformImage = ttk.Label(
    root,
    # image=photo,
    text='Transform',
    compound='top'
)
transformImage.grid(column=1, row=1, padx=5, pady=5)
cautionLabel = ttk.Label(
    root,
    text='Caution: This image has been resized to (450, 350), which is different to the original image size',
    background='white',
    foreground='red',
    justify=tk.CENTER
)
cautionLabel.grid(column=0, row=0, columnspan=2)

def create_config_frame(container):
    frame = ttk.Frame(container)

    frame.columnconfigure(0, weight=1)

    ttk.Button(frame, text='Find Next').grid(column=0, row=0)
    ttk.Button(frame, text='Replace').grid(column=0, row=1)
    ttk.Button(frame, text='Replace All').grid(column=0, row=2)
    ttk.Button(frame, text='Cancel').grid(column=0, row=3)

    for widget in frame.winfo_children():
        widget.grid(padx=0, pady=3)

    return frame



root.mainloop()