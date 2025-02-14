from PIL import Image, ImageTk
import tkinter as tk

BG_COLOR_INIT = "white"

class ImageViewer:
    def __init__(self, root, image_path):
        self.root = root
        self.image_path = image_path

        self.keep_aspect_ratio = tk.BooleanVar(value=True)
        self.use_black_bg = tk.BooleanVar(value=False)

        #self.root.overrideredirect(True)

        self.img = Image.open(image_path)
        self.img_original = self.img.copy() 
        self.photo = ImageTk.PhotoImage(self.img)

        self.canvas = tk.Canvas(root, bg=BG_COLOR_INIT, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Configure>", self.resize_image)
        self.root.bind("q", self.quit_dummy)
        self.root.bind("o", self.toggle_keep_aspect_ratio)
        self.root.bind("a", self.toggle_keep_aspect_ratio)
        self.root.bind("r", self.resize_window_to_image)
        self.root.bind("b", self.toggle_use_black_bg)

        self.menu = tk.Menu(root, tearoff=0)
        self.menu.add_command(label="Open... (O)")
        self.menu.add_checkbutton(label="Keep aspect ratio (A)", variable=self.keep_aspect_ratio, command=self.toggle_keep_aspect_ratio)
        self.menu.add_command(label="Resize window to image (R)", command=self.resize_window_to_image)
        self.menu.add_checkbutton(label="Use black background (B)", variable=self.use_black_bg, command=self.toggle_use_black_bg)
        self.menu.add_separator()
        self.menu.add_command(label="About")
        self.menu.add_command(label="Quit (Q)", command=self.quit_dummy)
        self.root.bind("<Button-3>", self.show_menu)

        self.update_image()

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

    def toggle_keep_aspect_ratio(self, event=None):
        if event:
            self.keep_aspect_ratio.set(not self.keep_aspect_ratio.get())
        self.resize_image()

    def resize_window_to_image(self, event=None):
        if self.keep_aspect_ratio.get():
            new_size = self.get_size()
            self.root.geometry(f"{new_size[0]}x{new_size[1]}")

    def update_image(self):
        self.canvas.delete("all")
        self.canvas.create_image(self.canvas.winfo_width() // 2, 
                                 self.canvas.winfo_height() // 2, 
                                 anchor=tk.CENTER, image=self.photo)
        
    def get_size(self):
        win_w, win_h = self.root.winfo_width(), self.root.winfo_height()
        img_w, img_h = self.img_original.size

        if self.keep_aspect_ratio.get():
            scale = min(win_w / img_w, win_h / img_h)
            new_size = (int(img_w * scale), int(img_h * scale))
        else:
            new_size = (win_w, win_h)

        return new_size

    def resize_image(self, event=None):
        new_size = self.get_size()
        resized_img = self.img_original.resize(new_size, Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(resized_img)

        self.update_image()

root = tk.Tk()
root.title("plainIMG")
root.geometry("800x600")
root.configure(bg=BG_COLOR_INIT)

image_path = "image.png"
viewer = ImageViewer(root, image_path)

root.mainloop()
