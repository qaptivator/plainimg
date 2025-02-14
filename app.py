from PIL import Image, ImageTk
import tkinter as tk

class ImageViewer:
    def __init__(self, root, image_path):
        self.root = root
        self.image_path = image_path
        self.aspect_ratio = True  # Toggle for keeping aspect ratio

        self.img = Image.open(image_path)
        self.img_original = self.img.copy()  # Keep original for resizing
        self.photo = ImageTk.PhotoImage(self.img)

        self.canvas = tk.Canvas(root, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Configure>", self.resize_image)
        self.root.bind("a", self.toggle_aspect_ratio)  # Toggle aspect ratio with 'A' key

        self.update_image()

    def update_image(self):
        self.canvas.delete("all")
        self.canvas.create_image(self.canvas.winfo_width() // 2, 
                                 self.canvas.winfo_height() // 2, 
                                 anchor=tk.CENTER, image=self.photo)

    def resize_image(self, event=None):
        win_w, win_h = self.root.winfo_width(), self.root.winfo_height()
        img_w, img_h = self.img_original.size

        if self.aspect_ratio:
            scale = min(win_w / img_w, win_h / img_h)
            new_size = (int(img_w * scale), int(img_h * scale))
        else:
            new_size = (win_w, win_h)

        resized_img = self.img_original.resize(new_size, Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(resized_img)

        self.update_image()

    def toggle_aspect_ratio(self, event=None):
        self.aspect_ratio = not self.aspect_ratio
        self.resize_image()

# Initialize
root = tk.Tk()
root.title("Minimal Image Viewer")
root.geometry("800x600")
root.configure(bg="black")  # Background color

image_path = "image.jpg"  # Change this to your image
viewer = ImageViewer(root, image_path)

root.mainloop()
