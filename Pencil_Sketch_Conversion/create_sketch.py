import cv2
import numpy 
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk

# Ditionary to store PIL images
images = {"original": None, "sketch": None}

def open_file():
    filepath = filedialog.askopenfilename()
    if not filepath:
        return
    img = cv2.imread(filepath) 
    display_image(img, original=True)
    sketch_img = convert_to_sketch(img)
    display_image(sketch_img, original=False)

def convert_to_sketch(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted_gray_img = cv2.bitwise_not(gray_img)
    blurred_img = cv2.GaussianBlur(inverted_gray_img, (21, 21), 0)
    inverted_blurred_img = cv2.bitwise_not(blurred_img)
    sketch_img = cv2.divide(gray_img, inverted_blurred_img, scale=256.0)
    return sketch_img

def display_image(img, original):
    max_width, max_height = 480, 480 # Set the max width and height for the image display

    # Resize the image if it exceeds the max dimensions
    height, width = img.shape[:2]
    scaling_factor = max(max_width / width, max_height / height)
    if scaling_factor < 1:
        new_width = int(width * scaling_factor)
        new_height = int(height * scaling_factor)
        img = cv2.resize(img, (new_width, new_height))

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) if original else img
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)

    # Store the PIL image in the dictionary
    if original:
        images["original"] = img_pil
    else:
        images["sketch"] = img_pil  

    label = original_image_label if original else sketch_image_label
    label.config(image=img_tk)
    label.image = img_tk


def save_sketch():
    if images["sketch"] is None:
        messagebox.showerror("Error", "No sketch to save!")
        return
    
    sketch_filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if not sketch_filepath:
        return
    # Save the PIL image (sketch) to the file
    images["sketch"].save(sketch_filepath, "PNG")
    messagebox.showinfo("Saved", "Sketch saved to {}!".format(sketch_filepath))


app = tk.Tk()
app.title('Pencil Sketch Converter')

frame = tk.Frame(app)
frame.pack(padx=10, pady=10)

original_image_label = tk.Label(frame)
original_image_label.grid(row=0, column=0, padx=5, pady=5)
sketch_image_label = tk.Label(frame)
sketch_image_label.grid(row=0, column=1, padx=5, pady=5)

btn_frame = tk.Frame(app)
btn_frame.pack(pady=10)

open_button = tk.Button(btn_frame, text="Open Image", command=open_file)
open_button.grid(row=0, column=0, padx=5)

save_button = tk.Button(btn_frame, text="Save Sketch", command=save_sketch)
save_button.grid(row=0, column=1, padx=5)

app.mainloop()