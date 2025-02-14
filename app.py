from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
import sys
import os

VERSION_NUMBER = "0.1"
DEFAULT_SIZE = (800, 600)
BG_COLOR_INIT = "white"
GLOBAL_FONT = ("Consolas", 24, "bold")

class ImageViewer:
    def __init__(self, root, image_path=None):
        self.root = root
        self.image_path = image_path
        #self.image_opened = self.image_path is not None

        self.keep_aspect_ratio = tk.BooleanVar(value=True)
        self.use_black_bg = tk.BooleanVar(value=False)

        #self.root.overrideredirect(True)

        #self.img = Image.open(image_path)
        #self.img_original = self.img.copy() 
        #self.photo = ImageTk.PhotoImage(self.img)
        self.open_image()

        self.canvas = tk.Canvas(root, width=DEFAULT_SIZE[0], height=DEFAULT_SIZE[1], bg=BG_COLOR_INIT, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Configure>", self.resize_image)
        self.root.bind("q", self.quit_dummy)
        self.root.bind("o", self.open_image_command)
        self.root.bind("a", self.toggle_keep_aspect_ratio)
        self.root.bind("r", self.resize_window_to_image)
        self.root.bind("b", self.toggle_use_black_bg)

        self.menu = tk.Menu(root, tearoff=0)
        self.menu.add_command(label="Open Image... (O)", command=self.open_image_command)
        self.menu.add_checkbutton(label="Keep aspect ratio (A)", variable=self.keep_aspect_ratio, command=self.toggle_keep_aspect_ratio)
        self.menu.add_command(label="Resize window to image (R)", command=self.resize_window_to_image)
        self.menu.add_checkbutton(label="Use black background (B)", variable=self.use_black_bg, command=self.toggle_use_black_bg)
        self.menu.add_separator()
        self.menu.add_command(label="About")
        self.menu.add_command(label="Quit (Q)", command=self.quit_dummy)
        self.root.bind("<Button-3>", self.show_menu)

        self.update_canvas()

    def image_opened(self):
        return self.image_path is not None

    # MENU BUTTONS
    def quit_dummy(self, event=None):
        self.root.quit()

    def show_menu(self, event):
        self.menu.tk_popup(event.x_root, event.y_root)

    def toggle_use_black_bg(self, event=None):
        if event:
            self.use_black_bg.set(not self.use_black_bg.get())
        
        if self.use_black_bg.get():
            self.canvas.config(bg="black")
        else:
            self.canvas.config(bg="white")
        
        self.update_canvas()

    def toggle_keep_aspect_ratio(self, event=None):
        if event:
            self.keep_aspect_ratio.set(not self.keep_aspect_ratio.get())
        
        self.resize_image()

    def resize_window_to_image(self, event=None):
        if self.keep_aspect_ratio.get() and self.image_opened():
            new_size = self.get_size()
            self.root.geometry(f"{new_size[0]}x{new_size[1]}")
        
        self.update_canvas()

    def open_image_command(self, event=None):
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.tiff")]
        )
        # in this case, we just ignore it, because the user couldve clicked "Cancel"
        if file_path:
            if os.path.exists(file_path):
                self.image_path = file_path
                self.open_image()
            else:
                print(f"[ERROR]: Image path not found '{image_path}', provided in the file dialog! Continuing with imageless mode.")
            

    # IMAGE HANDLING
    def open_image(self):
        if not self.image_opened():
            return

        self.img = Image.open(self.image_path)
        self.img_original = self.img.copy() 
        self.photo = ImageTk.PhotoImage(self.img)

        self.resize_image()

    def resize_image(self, event=None):
        if not self.image_opened():
            self.update_canvas()
            return
        
        new_size = self.get_size()
        resized_img = self.img_original.resize(new_size, Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(resized_img)

        self.update_canvas()

    def update_canvas(self):
        self.canvas.delete("all")

        # apparently on initalization of tkinter window, winfo_width and height return 0 (or 1)
        if self.image_opened():
            self.canvas.create_image(self.canvas.winfo_width() // 2, 
                self.canvas.winfo_height() // 2, 
                anchor=tk.CENTER, image=self.photo)
        else:
            actual_size = (self.canvas.winfo_width(), self.canvas.winfo_height())
            if (actual_size[0] == 0 or actual_size[1] == 0) or (actual_size[0] == 1 or actual_size[1] == 1):
                actual_size = DEFAULT_SIZE
            
            self.canvas.create_text(
                actual_size[0] // 2, actual_size[1] // 2,
                text=f"plainIMG v{VERSION_NUMBER}\nOpen Menu  [Right Click]\nOpen Image [O]\nQuit       [Q]",
                font=GLOBAL_FONT,
                fill=("white" if self.use_black_bg.get() else "black"),
                #justify=tk.CENTER
            )

        
    def get_size(self):
        win_w, win_h = self.root.winfo_width(), self.root.winfo_height()
        img_w, img_h = self.img_original.size

        if self.keep_aspect_ratio.get():
            scale = min(win_w / img_w, win_h / img_h)
            new_size = (int(img_w * scale), int(img_h * scale))
        else:
            new_size = (win_w, win_h)

        return new_size

if __name__ == "__main__":
    root = tk.Tk()
    root.title("plainIMG")
    root.geometry(f"{DEFAULT_SIZE[0]}x{DEFAULT_SIZE[1]}")
    root.configure(bg=BG_COLOR_INIT)

    # imageless is when the application starts without an image provided at the start, which causes the starting text to display
    image_path = None
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        if not os.path.exists(image_path):
            print(f"[ERROR]: Image path not found '{image_path}', provided in the first argument! Starting with imageless mode.")
            image_path = None


    # FOR DEBUG WHILE DEVELOPING
    #image_path = "image.png"

    viewer = ImageViewer(root, image_path)

    root.mainloop()
