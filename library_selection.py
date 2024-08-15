import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from Add_Member import AddMember
import psycopg2
from tempLibraryInterface import LibraryInterface

class LibrarySelectionInterface:
    def __init__(self, root, previous_interface):
        self.root = root
        self.previous_interface = previous_interface
        self.selected_member_type = tk.StringVar()
        self.selected_library = tk.StringVar()
        self.create_library_selection_frame()
    
    def create_library_selection_frame(self):
        self.library_selection_frame = ttk.Frame(self.root)
        self.library_selection_frame.grid(sticky='nsew')
        
        self.library_selection_frame.rowconfigure(0, weight=1)
        self.library_selection_frame.rowconfigure(1, weight=10)
        self.library_selection_frame.rowconfigure(2, weight=10)
        self.library_selection_frame.rowconfigure(3, weight=1)
        self.library_selection_frame.rowconfigure(4, weight=10)
        
        
        self.library_selection_frame.columnconfigure(0, weight=1)
        self.library_selection_frame.columnconfigure(1, weight=1)
        
        # Load and place logo image
        # self.load_logo_image()
        
        # Top Logo Image
        # logo_label = ttk.Label(self.library_selection_frame, image=self.logo_img)
        # logo_label.grid(row=0, column=0, columnspan=2, pady=10, sticky='ew')
        self.institute_name_label=tk.Label(self.library_selection_frame,text="INDIAN INSTITUTE OF TECHNOLOGY PALAKKAD \n LOGIN PAGE", font=("Helvetica", 40),bg="purple")
        self.institute_name_label.grid(row=0,column=0,columnspan=2,sticky='ew',padx=20,pady=20)




        # Library buttons
        self.button1_frame = ttk.Frame(self.library_selection_frame)
        self.button1_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky='n')
        
        self.button1_frame.columnconfigure(0, weight=1)
        self.button1_frame.columnconfigure(1, weight=1)
        
        style = ttk.Style()
        style.configure('TButton', font=("Helvetica", 16), padding=10, relief="flat", background='#FFFFFF')
        # style.map('TButton',
        #           background=[('active', '#FFDD33')],
        #           foreground=[('active', 'white')],
        #           relief=[('pressed', 'groove'), ('!pressed', 'ridge')])

        # ttk.Button( self.button1_frame, text="Nila Library", command=self.open_nila_library, width=20).grid(row=0, column=0, padx=40, pady=20)
        # ttk.Button( self.button1_frame, text="Sahyadri Library", command=self.open_sahyadri_library, width=20).grid(row=0, column=1, padx=40, pady=20)
        ttk.Label(self.button1_frame, text="Select Library:", font=("Helvetica", 25)).grid(row=0, column=0, padx=40, pady=20, sticky='e')

        # Combobox for Library Selection
        self.library_combobox = ttk.Combobox(self.button1_frame, textvariable=self.selected_library, state="readonly", font=("Helvetica", 20), width=30)
        self.library_combobox.grid(row=0, column=1, padx=40, pady=20, sticky='w')

        # Button to Confirm Selection
        ttk.Button(self.button1_frame, text="Select", command=self.select_library, width=20).grid(row=1, column=0, columnspan=2, padx=40, pady=20)

        # Populate the combobox with library names from the database
        self.populate_library_combobox()
        
        self.button2_frame = ttk.Frame(self.library_selection_frame)
        self.button2_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky='n')
        
        Add_people_label=ttk.Button(self.button2_frame,text="Admin portal",command=self.show_details,width=25)
        Add_people_label.grid(row=0, column=0, columnspan=2, padx=40, pady=20)
        # Member type selection
        
        
        
        self.button0_frame = ttk.Frame(self.library_selection_frame)
        self.button0_frame.grid(row=2, column=0, columnspan=2, pady=20, sticky='n')
        self.button0_frame.grid_remove()
        tk.Label(self.button0_frame, text="Username", font=("Helvetica", 25)).grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.username_entry = tk.Entry(self.button0_frame, font=("Helvetica", 20))
        self.username_entry.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
        
        tk.Label(self.button0_frame, text="Password", font=("Helvetica", 25)).grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.password_entry = tk.Entry(self.button0_frame, show="*", font=("Helvetica", 20))
        self.password_entry.grid(row=2, column=1, padx=10, pady=10, sticky='ew')
        
        self.show_password_var = tk.IntVar()
        tk.Checkbutton(self.button0_frame, text="Show", variable=self.show_password_var, command=self.toggle_password, font=("Helvetica", 16)).grid(row=2, column=2, columnspan=2, pady=10)
        tk.Button(self.button0_frame, text="Login", command=self.login, font=("Helvetica", 16)).grid(row=3, column=0, columnspan=2, pady=10)
        
        
        
        self.button3_frame = ttk.Frame(self.library_selection_frame)
        self.button3_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky='n')
        self.button3_frame.grid_remove()
        member_type_label = ttk.Label(self.button3_frame, text="Select Member Type:")
        member_type_label.grid(row=1, column=0, columnspan=2, padx=40, pady=10)
        self.member_type_combobox = ttk.Combobox(self.button3_frame, textvariable=self.selected_member_type, state="readonly", font=("Helvetica", 14))
        self.member_type_combobox['values'] = ["student", "Faculty", "Staff", "External Users", "Alumni", "Family"]
        self.member_type_combobox.grid(row=2, column=0, columnspan=2, padx=40, pady=10)
        # Add Single Member button
        self.add_single_member_button = ttk.Button(self.button3_frame, text="Add Single Member", command=self.run_add_single_member_command, width=25)
        self.add_single_member_button.grid(row=3, column=0, columnspan=2, padx=40, pady=20)
        # Member List Upload button
        self.add_multi_member_button = ttk.Button(self.button3_frame, text="Member List Upload", command=self.run_add_multi_member_command, width=25)
        self.add_multi_member_button.grid(row=4, column=0, columnspan=2, padx=40, pady=20)
        
        
        
        # Back button
        self.button4_frame = ttk.Frame(self.library_selection_frame)
        self.button4_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky='n')
        ttk.Button(self.button4_frame, text="Back", command=self.go_back, width=20).grid(row=5, column=0, columnspan=2, padx=40, pady=20)

    
    def populate_library_combobox(self):
        try:
            # Connect to the database
            conn = psycopg2.connect(
                dbname="library_dbms",
                user="postgres",
                password="S@i*iran2004",
                host="10.32.11.146",
                port="5432"
            )
            cursor = conn.cursor()

            # Execute query to get library names
            cursor.execute("SELECT library_name FROM library")
            libraries = cursor.fetchall()

            # Extract library names from the query result and set them in the combobox
            library_names = [lib[0] for lib in libraries]
            self.library_combobox['values'] = library_names

            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load libraries: {e}")

    def select_library(self):
        selected_library = self.selected_library.get()
        if selected_library:
            self.open_library_interface(selected_library)
        else:
            messagebox.showerror("Error", "Please select a library.")
    def open_library_interface(self, library_name):
        self.library_selection_frame.destroy()
        LibraryInterface(self.root, library_name, self)


    
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
                host ="10.32.11.146",
                port="5432"
            )
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users WHERE username=%s AND password=%s', (username, password))
            result = cursor.fetchone()
            
            conn.close()
            
            if result:
                self.show_options()
                print("correct user")
                self.username_entry=""
                self.password_entry=""
            else:
                self.return_initial()
                messagebox.showerror("Error", "Invalid username or password")
        except Exception as e:
            messagebox.showerror("Error", f"Database connection failed: {e}")
    def show_details(self):
        self.button2_frame.grid_forget()
        self.show_login()
    
    def show_login(self):
        self.button0_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky='n')
    def show_options(self):
        self.button0_frame.grid_forget()
        self.button3_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky='n')
    def return_initial(self):
        self.button0_frame.grid_forget()
        self.button2_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky='n')
    def add1(self):
        self.library_selection_frame.destroy()
        AddMember(self.root, self,"single", self.selected_member_type.get())
    
    def add_multi(self):
        self.library_selection_frame.destroy()
        AddMember(self.root, self,"multi", self.selected_member_type.get())

    def load_logo_image(self):
        base_dir = os.path.dirname(__file__)
        logo_image_path = os.path.join("images", "logotext.png")
        print(logo_image_path)

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
        
        if self.selected_member_type.get():
            self.add1()
        else:
            messagebox.showerror("Error", "Please select a member type first.")
            

    def run_add_multi_member_command(self):
        if self.selected_member_type.get():
            self.add_multi()
        else:
            messagebox.showerror("Error", "Please select a member type first.")
        

if __name__ == "__main__":
    root = tk.Tk()
    login_interface = LoginInterface(root)
    app = LibrarySelectionInterface(root, login_interface)
    root.mainloop()
