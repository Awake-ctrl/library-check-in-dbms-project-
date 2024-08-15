import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import pandas as pd
import psycopg2
import subprocess
from datetime import datetime

class AddMember:
    def __init__(self, root, previous_interface, no_of, member_type):
        self.root = root
        self.previous_interface = previous_interface
        self.member_type = member_type
        if no_of == "single":
            self.create_add_member_frame()
        else:
            self.create_add_members_frame()

    def create_add_member_frame(self):
        self.add_frame = tk.Frame(self.root)
        self.add_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        tk.Label(self.add_frame, text=f"{self.member_type} was selected", font=("Helvetica", 20)).pack(pady=10)

        # Entries for member details
        self.create_label_entry(self.add_frame, "id:")
        self.create_label_entry(self.add_frame, "name:")
        self.create_program_combobox(self.add_frame)
        self.create_department_combobox(self.add_frame)
        self.create_photo_entry(self.add_frame)
        self.create_valid_year_combobox(self.add_frame)

        # Submit button
        self.submit_button = tk.Button(self.add_frame, text="Submit", command=self.submit_member, bg="black", fg="white", bd=0, highlightthickness=0, font=("Helvetica", 14))
        self.submit_button.pack(pady=10)

        # Back button
        self.back_button = tk.Button(self.add_frame, text="Back", command=self.go_back, bg="black", fg="white", bd=0, highlightthickness=0, font=("Helvetica", 14))
        self.back_button.pack(pady=10)

    def create_label_entry(self, frame, label_text):
        container = tk.Frame(frame)
        container.pack(fill=tk.X, pady=10,padx=50)

        tk.Label(container, text=label_text, width=10, anchor='w', font=("Helvetica", 14)).pack(side=tk.LEFT)
        entry = tk.Entry(container, font=("Helvetica", 14))
        entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        label_text=label_text.split(":")[0].lower()
        label_text=label_text.split()
        text=""
        for i in range(len(label_text)):
            text+=label_text[i]+"_"
        label_text=text
        print(label_text)
        setattr(self, label_text + "entry", entry)

    def create_program_combobox(self, frame):
        container = tk.Frame(frame)
        container.pack(fill=tk.X, pady=10,padx=50)

        tk.Label(container, text="Program:", width=15, anchor='w', font=("Helvetica", 14)).pack(side=tk.LEFT)
        self.program_combobox = ttk.Combobox(container, font=("Helvetica", 14))
        self.program_combobox.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.programs = ["UG", "PG", "Research Scholar"]
        self.program_combobox['values'] = self.programs

        self.program_combobox.bind('<KeyRelease>', self.update_program_combobox)

    def update_program_combobox(self, event):
        typed = self.program_combobox.get().lower()
        if typed == '':
            data = self.programs
        else:
            data = [item for item in self.programs if typed in item.lower()]
        self.program_combobox['values'] = data

    def create_department_combobox(self, frame):
        container = tk.Frame(frame)
        container.pack(fill=tk.X, pady=10,padx=50)

        tk.Label(container, text="Department:", width=15, anchor='w', font=("Helvetica", 14)).pack(side=tk.LEFT)
        self.department_combobox = ttk.Combobox(container, font=("Helvetica", 14))
        self.department_combobox.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.departments = [
            "Biological Science and Engineering", "Chemistry", "Civil Engineering", 
            "Computer Science and Engineering", "Data Science", "Electrical Engineering", 
            "ESSENCE", "Humanities and Social Sciences", "Mathematics", 
            "Mechanical Engineering", "Physics", "Geotechnical Engineering", 
            "Computing and Mathematics", "Power Electronics and Power Systems", 
            "Manufacturing and Materials Engineering", "System-on-Chip Design"
        ]
        self.department_combobox['values'] = self.departments

        self.department_combobox.bind('<KeyRelease>', self.update_department_combobox)

    def update_department_combobox(self, event):
        typed = self.department_combobox.get().lower()
        if typed == '':
            data = self.departments
        else:
            data = [item for item in self.departments if typed in item.lower()]
        self.department_combobox['values'] = data

    def create_photo_entry(self, frame):
        container = tk.Frame(frame)
        container.pack(fill=tk.X, pady=5)

        tk.Label(container, text="Photo:", width=15, anchor='w', font=("Helvetica", 14)).pack(side=tk.LEFT)
        self.photo_entry = tk.Entry(container, font=("Helvetica", 14))
        self.photo_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.photo_browse_button = tk.Button(container, text="Browse", command=self.browse_photo, bg="black", fg="white", bd=0, highlightthickness=0, font=("Helvetica", 14))
        self.photo_browse_button.pack(side=tk.LEFT, padx=5)

    def browse_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.JPG *.PNG")])
        if file_path:
            self.photo_entry.delete(0, tk.END)
            self.photo_entry.insert(0, file_path)

    def create_valid_year_combobox(self, frame):
        container = tk.Frame(frame)
        container.pack(fill=tk.X, pady=5)

        tk.Label(container, text="Valid Year:", width=15, anchor='w', font=("Helvetica", 14)).pack(side=tk.LEFT)
        self.valid_year_combobox = ttk.Combobox(container, font=("Helvetica", 14))
        current_year = datetime.now().year
        self.valid_year_combobox['values'] = list(range(current_year, current_year + 26))
        self.valid_year_combobox.pack(side=tk.LEFT, expand=True, fill=tk.X)

    def create_add_members_frame(self):
        self.add_frame = tk.Frame(self.root)
        self.add_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        tk.Label(self.add_frame, text=f"{self.member_type} was selected", font=("Helvetica", 20)).pack(pady=10)

        self.create_label_entry(self.add_frame, "CSV File Path:")
        self.csv_browse_button = tk.Button(self.add_frame, text="Browse", command=self.browse_csv, bg="black", fg="white", bd=0, highlightthickness=0, font=("Helvetica", 14))
        self.csv_browse_button.pack(pady=10)

        self.create_label_entry(self.add_frame, "Photo Folder Path:")
        self.photo_browse_button = tk.Button(self.add_frame, text="Browse", command=self.browse_photo_folder, bg="black", fg="white", bd=0, highlightthickness=0, font=("Helvetica", 14))
        self.photo_browse_button.pack(pady=10)

        self.submit_button = tk.Button(self.add_frame, text="Submit", command=self.submit_bulk_members, bg="black", fg="white", bd=0, highlightthickness=0, font=("Helvetica", 14))
        self.submit_button.pack(pady=10)

        self.back_button = tk.Button(self.add_frame, text="Back", command=self.go_back, bg="black", fg="white", bd=0, highlightthickness=0, font=("Helvetica", 14))
        self.back_button.pack(pady=10)

    def browse_csv(self):
        self.csv_file_path_entry.delete(0, tk.END)
        csv_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        self.csv_file_path_entry.insert(0, csv_path)

    def browse_photo_folder(self):
        self.photo_folder_path_entry.delete(0, tk.END)
        photo_folder_path = filedialog.askdirectory()
        self.photo_folder_path_entry.insert(0, photo_folder_path)

    def submit_member(self):
        member_id = self.id_entry.get()
        name = self.name_entry.get()
        program = self.program_combobox.get()
        department = self.department_combobox.get()
        photo = self.photo_entry.get()
        valid_year = self.valid_year_combobox.get()

        if not all([member_id, name, program, department, photo, valid_year]):
            messagebox.showerror("Input Error", "All fields are required.")
            return

        try:
            conn = psycopg2.connect(
                dbname="library_dbms",
                user="postgres",
                password="S@i*iran2004",
                host="localhost",
                port="5432"
            )
            cursor = conn.cursor()

            sql = f"""INSERT INTO {self.member_type} (id, name, department, program, photo, valid_year)
                     VALUES (%s, %s, %s, %s, %s, %s)
                     ON CONFLICT (id) DO UPDATE
                     SET name = EXCLUDED.name,
                         department = EXCLUDED.department,
                         program = EXCLUDED.program,
                         photo = EXCLUDED.photo,
                         valid_year = EXCLUDED.valid_year"""
            cursor.execute(sql, (member_id, name, department, program, photo, valid_year))
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Member Added", f"Member {name} added successfully.")
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def submit_bulk_members(self):
        csv_path = self.csv_file_path_entry.get()
        photo_folder_path = self.photo_folder_path_entry.get()

        if not all([csv_path, photo_folder_path]):
            messagebox.showerror("Input Error", "Both CSV file path and photo folder path are required.")
            return

        try:
            subprocess.run(["python", "insertdata.py", csv_path, photo_folder_path])
            messagebox.showinfo("Bulk Members Added", "All members have been processed.")
        except Exception as e:
            messagebox.showerror("Processing Error", f"An error occurred: {e}")

    def go_back(self):
        self.add_frame.destroy()
        self.previous_interface.create_library_selection_frame()
        self.previous_interface.root.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Library Management System")
    root.geometry("800x600")

    class LibrarySelectionInterface:
        def __init__(self, root, login_interface):
            self.root = root

        def create_library_selection_frame(self):
            pass

    class LoginInterface:
        def __init__(self, root):
            self.root = root

    login_interface = LoginInterface(root)
    app = LibrarySelectionInterface(root, login_interface)
    no_of = "single"
    member_type = "student"
    b = AddMember(root, app, no_of, member_type)
    root.mainloop()
