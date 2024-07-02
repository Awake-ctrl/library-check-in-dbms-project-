import os
import tkinter as tk
from PIL import Image, ImageTk
from library_interface import LibraryInterface

class LibrarySelectionInterface:
    def __init__(self, root, previous_interface):
        self.root = root
        self.previous_interface = previous_interface
        self.create_library_selection_frame()
    
    def create_library_selection_frame(self):
        self.library_selection_frame = tk.Frame(self.root)
        self.library_selection_frame.grid(sticky='nsew')
        
        self.library_selection_frame.rowconfigure(0, weight=1)
        self.library_selection_frame.rowconfigure(1, weight=10)
        self.library_selection_frame.columnconfigure(0, weight=1)
        self.library_selection_frame.columnconfigure(1, weight=1)
        
        # Load and place logo image
        self.load_logo_image()
        
        # Top Logo Image
        logo_label = tk.Label(self.library_selection_frame, image=self.logo_img)
        logo_label.grid(row=0, column=0, columnspan=2, pady=10, sticky='ew')

        # Library buttons
        button_frame = tk.Frame(self.library_selection_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=20, sticky='n')
        
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        tk.Button(button_frame, text="Nila Library", command=self.open_nila_library, font=("Helvetica", 16), width=20).grid(row=0, column=0, padx=20, pady=10)
        tk.Button(button_frame, text="Sahyadri Library", command=self.open_sahyadri_library, font=("Helvetica", 16), width=20).grid(row=0, column=1, padx=20, pady=10)
        
        # Back button
        tk.Button(button_frame, text="Back", command=self.go_back, font=("Helvetica", 16), width=20).grid(row=1, column=0, columnspan=2, padx=20, pady=10)

    def load_logo_image(self):
        base_dir = os.path.dirname(__file__)
        logo_image_path = os.path.join(base_dir, "images", "logotext.png")

        self.logo_img = Image.open(logo_image_path)
        self.logo_img = self.logo_img.resize((1366, 100), Image.Resampling.LANCZOS)
        self.logo_img = ImageTk.PhotoImage(self.logo_img)
    
    def open_nila_library(self):
        self.library_selection_frame.destroy()
        LibraryInterface(self.root, "Nila", self)
    
    def open_sahyadri_library(self):
        self.library_selection_frame.destroy()
        LibraryInterface(self.root, "Sahyadri", self)
    
    def go_back(self):
        self.library_selection_frame.destroy()
        self.previous_interface.create_login_frame()

if __name__ == "__main__":
    root = tk.Tk()
    login_interface = LoginInterface(root)
    app = LibrarySelectionInterface(root, login_interface)
    root.mainloop()
