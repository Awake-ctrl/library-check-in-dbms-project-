import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from library_interface import LibraryInterface
from Add_Member import add_member

class LibrarySelectionInterface:
    def __init__(self, root, previous_interface):
        self.root = root
        self.previous_interface = previous_interface
        self.selected_member_type = None
        self.create_library_selection_frame()
    
    def create_library_selection_frame(self):
        self.library_selection_frame = ttk.Frame(self.root)
        self.library_selection_frame.grid(sticky='nsew')
        
        self.library_selection_frame.rowconfigure(0, weight=1)
        self.library_selection_frame.rowconfigure(1, weight=10)
        self.library_selection_frame.columnconfigure(0, weight=1)
        self.library_selection_frame.columnconfigure(1, weight=1)
        
        # Load and place logo image
        self.load_logo_image()
        
        # Top Logo Image
        logo_label = ttk.Label(self.library_selection_frame, image=self.logo_img)
        logo_label.grid(row=0, column=0, columnspan=2, pady=10, sticky='ew')

        # Library buttons
        button_frame = ttk.Frame(self.library_selection_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=20, sticky='n')
        
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        style = ttk.Style()
        style.configure('TButton', font=("Helvetica", 16), padding=10, relief="flat", background='#FFFFFF')
        style.map('TButton',
                  background=[('active', '#FFDD33')],
                  foreground=[('active', 'white')],
                  relief=[('pressed', 'groove'), ('!pressed', 'ridge')])

        ttk.Button(button_frame, text="Nila Library", command=self.open_nila_library, width=20).grid(row=0, column=0, padx=40, pady=20)
        ttk.Button(button_frame, text="Sahyadri Library", command=self.open_sahyadri_library, width=20).grid(row=0, column=1, padx=40, pady=20)
        
        # Add single Member button with hover options
        self.add_single_member_button = ttk.Button(button_frame, text="Add Single Member", command=self.run_add_single_member_command, width=25)
        self.add_single_member_button.grid(row=1, column=0, columnspan=2, padx=40, pady=20)
        self.add_single_member_button.bind("<Enter>", self.show_single_member_options)
        self.add_single_member_button.bind("<Leave>", self.hide_options_menu)
        
        # Member List Upload button with hover options
        self.add_multi_member_button = ttk.Button(button_frame, text="Member List Upload", command=self.run_add_multi_member_command, width=25)
        self.add_multi_member_button.grid(row=2, column=0, columnspan=2, padx=40, pady=20)
        self.add_multi_member_button.bind("<Enter>", self.show_multi_member_options)
        self.add_multi_member_button.bind("<Leave>", self.hide_options_menu)
        
        # Back button
        ttk.Button(button_frame, text="Back", command=self.go_back, width=20).grid(row=3, column=0, columnspan=2, padx=40, pady=20)

    def add1(self):
        self.library_selection_frame.destroy()
        add_member(self.root, self,"single", self.selected_member_type)

    def add_multi(self):
        self.library_selection_frame.destroy()
        add_member(self.root, self,"multi", self.selected_member_type)

    def show_single_member_options(self, event):
        self.show_options_menu(event, self.set_selected_member_type)

    def show_multi_member_options(self, event):
        self.show_options_menu(event, self.set_selected_member_type)

    def set_selected_member_type(self, member_type):
        self.selected_member_type = member_type

    def show_options_menu(self, event, callback):
        self.options_menu = tk.Menu(self.root, tearoff=0)
        member_types = ["UG", "PG", "Research Scholar", "Faculty", "Staff", "External Users", "Alumni", "Family"]
        for member_type in member_types:
            self.options_menu.add_command(label=member_type, command=lambda mt=member_type: callback(mt))
        self.options_menu.post(event.x_root, event.y_root)

    def hide_options_menu(self, event):
        if self.options_menu:
            self.options_menu.unpost()
            self.options_menu = None

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

    def run_add_single_member_command(self):
        if self.selected_member_type:
            self.add1()
        else:
            messagebox.showerror("Error", "Please select a member type first.")
            

    def run_add_multi_member_command(self):
        if self.selected_member_type:
            self.add_multi()
        else:
            messagebox.showerror("Error", "Please select a member type first.")
        

if __name__ == "__main__":
    root = tk.Tk()
    login_interface = LoginInterface(root)
    app = LibrarySelectionInterface(root, login_interface)
    root.mainloop()
