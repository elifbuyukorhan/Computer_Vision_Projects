import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import Button, Label

def select_image():
    filePath = filedialog.askopenfilename()
    if not filePath:
        return
    image = cv2.imread(filePath)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    segment_image(image)

def segment_image(image):

    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    ret, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0
    markers = cv2.watershed(image, markers)
    image[markers == -1] = [255, 0, 0]
    

    display_segmented_image(image)


def display_segmented_image(image):
    max_width, max_height = 480, 480 # Set the max width and height for the image display

    # Resize the image if it exceeds the max dimensions
    height, width = image.shape[:2]
    scaling_factor = max(max_width / width, max_height / height)
    if scaling_factor < 1:
        new_width = int(width * scaling_factor)
        new_height = int(height * scaling_factor)
        image = cv2.resize(image, (new_width, new_height))
    cv2.imshow('Segmented Image', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

app = tk.Tk()
app.title("Image Segmentation Tool")

label = Label(app, text="Select an image to perform segmentation.")
label.pack(pady=10)

select_button = Button(app, text="Select Image", command=select_image)
select_button.pack(pady=10)

app.geometry("400x200")
app.mainloop()
