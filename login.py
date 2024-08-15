import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import psycopg2
from library_selection import LibrarySelectionInterface

class LoginInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("INDIAN INSTITUTE OF TECHNOLOGY PALAKKAD")
        self.root.state('zoomed')
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        
        self.create_login_frame()
    
    def create_login_frame(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.grid(sticky='nsew')
        
        self.login_frame.rowconfigure(0, weight=1)
        self.login_frame.rowconfigure(1, weight=10)
        self.login_frame.columnconfigure(0, weight=1)
        self.login_frame.columnconfigure(1, weight=2)
        
        # Load and place images
        
        # self.load_images()   dont want the image to be added 

        # Top Logo Image
        # logo_label = tk.Label(self.login_frame, image=self.logo_img)
        # logo_label.grid(row=0, column=0, columnspan=2, sticky='ew')

        # Left Image
        # left_image_label = tk.Label(self.login_frame, image=self.left_image)
        # left_image_label.grid(row=1, column=0, rowspan=4, sticky='ns')

        # Username and Password
        self.institute_name_label=tk.Label(self.login_frame,text="INDIAN INSTITUTE OF TECHNOLOGY PALAKKAD \n LOGIN PAGE", font=("Helvetica", 40),bg="purple")
        self.institute_name_label.grid(row=0,column=0,columnspan=2,sticky='ew',padx=20,pady=20)
        form_frame = tk.Frame(self.login_frame)
        form_frame.grid(row=1, column=0, rowspan=4, padx=10, pady=10, sticky='nsew')
        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=3)
        
        form_frame.rowconfigure(0, weight=1)
        form_frame.rowconfigure(1, weight=1)
        form_frame.rowconfigure(2, weight=1)
        form_frame.rowconfigure(3, weight=1)
        form_frame.rowconfigure(4, weight=1)  # Added to accommodate the exit button

        # Positioning the form elements in the middle
        tk.Label(form_frame, text="Username",fg="blue", font=("Helvetica", 25)).grid(row=1, column=0, padx=10, pady=5, sticky='ew')
        self.username_entry = tk.Entry(form_frame, font=("Helvetica", 20),border=None,borderwidth=2)
        self.username_entry.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
        
        tk.Label(form_frame, text="Password",fg="blue", font=("Helvetica", 25)).grid(row=2, column=0, padx=10, pady=5, sticky='ew')
        self.password_entry = tk.Entry(form_frame, show="*", font=("Helvetica", 20))
        self.password_entry.grid(row=2, column=1, padx=10, pady=10, sticky='ew')
        
        self.show_password_var = tk.IntVar()
        tk.Checkbutton(form_frame, text="Show", variable=self.show_password_var, command=self.toggle_password, font=("Helvetica", 16)).grid(row=2, column=2, columnspan=2, pady=10)
        
        tk.Button(form_frame, text="Login", command=self.login, font=("Helvetica", 16)).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Exit Button
        tk.Button(form_frame, text="Exit", command=self.exit_app, font=("Helvetica", 16)).grid(row=3, column=1, columnspan=2, pady=10,sticky="e")

    def load_images(self):
        base_dir = os.path.dirname(__file__)
        left_image_path = os.path.join( "images", "nila entry.jpg")
        logo_image_path = os.path.join("images", "logotext.png")
        print(left_image_path)
        print(logo_image_path)

        self.left_image = Image.open(left_image_path)
        self.left_image = self.left_image.resize((800, 700), Image.Resampling.LANCZOS)
        self.left_image = ImageTk.PhotoImage(self.left_image)

        self.logo_img = Image.open(logo_image_path)
        self.logo_img = self.logo_img.resize((1366, 100), Image.Resampling.LANCZOS)
        self.logo_img = ImageTk.PhotoImage(self.logo_img)

    def toggle_password(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            conn = psycopg2.connect(
                dbname="library_dbms",
                user="postgres",
                password="S@i*iran2004",
                # host="localhost",
                
                host="10.32.11.146",
                port="5432"
            )
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users WHERE username=%s AND password=%s', (username, password))
            result = cursor.fetchone()
            
            conn.close()
            
            if result:
                self.login_frame.destroy()
                LibrarySelectionInterface(self.root, self)
            else:
                messagebox.showerror("Error", "Invalid username or password")
        except Exception as e:
            messagebox.showerror("Error", f"Database connection failed: {e}")
    
    def exit_app(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginInterface(root)
    root.mainloop()
