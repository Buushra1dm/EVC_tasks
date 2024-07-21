import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        
        self.img_path = ""
        self.original_img = None
        self.processed_img = None
        self.history = []
        self.history_index = -1

        self.init_ui()

    def init_ui(self):
        # Load button
        load_btn = Button(self.root, text="Load Image", command=self.load_image)
        load_btn.pack(side=TOP, fill=X)

        # Save button
        save_btn = Button(self.root, text="Save Image", command=self.save_image)
        save_btn.pack(side=TOP, fill=X)

        # Transformation buttons
        rotate_btn = Button(self.root, text="Rotate", command=self.rotate_image)
        rotate_btn.pack(side=LEFT, fill=Y)

        resize_btn = Button(self.root, text="Resize", command=self.resize_image)
        resize_btn.pack(side=LEFT, fill=Y)

        brightness_btn = Button(self.root, text="Adjust Brightness", command=self.adjust_brightness)
        brightness_btn.pack(side=LEFT, fill=Y)

        contrast_btn = Button(self.root, text="Adjust Contrast", command=self.adjust_contrast)
        contrast_btn.pack(side=LEFT, fill=Y)

        blur_btn = Button(self.root, text="Blur", command=self.blur_image)
        blur_btn.pack(side=LEFT, fill=Y)

        undo_btn = Button(self.root, text="Undo", command=self.undo)
        undo_btn.pack(side=LEFT, fill=Y)

        redo_btn = Button(self.root, text="Redo", command=self.redo)
        redo_btn.pack(side=LEFT, fill=Y)

        self.img_label = Label(self.root)
        self.img_label.pack(side=BOTTOM, fill=BOTH, expand=True)

    def load_image(self):
        self.img_path = filedialog.askopenfilename()
        if self.img_path:
            self.original_img = cv2.imread(self.img_path)
            self.processed_img = self.original_img.copy()
            self.history = [self.processed_img.copy()]
            self.history_index = 0
            self.display_image()

    def save_image(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if save_path:
            cv2.imwrite(save_path, self.processed_img)
            print(f"Image saved as {save_path}")

    def rotate_image(self):
        if self.processed_img is not None:
            self.processed_img = cv2.rotate(self.processed_img, cv2.ROTATE_90_CLOCKWISE)
            self.update_history()
            self.display_image()

    def resize_image(self):
        if self.processed_img is not None:
            height, width = self.processed_img.shape[:2]
            self.processed_img = cv2.resize(self.processed_img, (width//2, height//2))
            self.update_history()
            self.display_image()

    def adjust_brightness(self):
        if self.processed_img is not None:
            self.processed_img = cv2.convertScaleAbs(self.processed_img, alpha=1, beta=50)
            self.update_history()
            self.display_image()

    def adjust_contrast(self):
        if self.processed_img is not None:
            lab = cv2.cvtColor(self.processed_img, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            cl = clahe.apply(l)
            limg = cv2.merge((cl, a, b))
            self.processed_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
            self.update_history()
            self.display_image()

    def blur_image(self):
        if self.processed_img is not None:
            self.processed_img = cv2.GaussianBlur(self.processed_img, (15, 15), 0)
            self.update_history()
            self.display_image()

    def undo(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.processed_img = self.history[self.history_index].copy()
            self.display_image()

    def redo(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.processed_img = self.history[self.history_index].copy()
            self.display_image()

    def update_history(self):
        self.history = self.history[:self.history_index+1]
        self.history.append(self.processed_img.copy())
        self.history_index += 1

    def display_image(self):
        img_rgb = cv2.cvtColor(self.processed_img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)
        self.img_label.config(image=img_tk)
        self.img_label.image = img_tk

if __name__ == "__main__":
    root = Tk()
    editor = ImageEditor(root)
    root.mainloop()
