import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd

class add_member:
    def __init__(self, root, previous_interface, no_of, member_type):
        self.root = root
        self.previous_interface = previous_interface
        self.member_type = member_type
        if no_of == "single":
            self.create_Add_member_frame()
        else:
            self.create_Add_members_frame()

    def create_Add_member_frame(self):
        self.add_frame = tk.Frame(self.root)
        self.add_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        tk.Label(self.add_frame, text=f"{self.member_type} was selected", font=("Helvetica", 20)).pack(pady=10)

        # Entries for member details
        self.create_label_entry(self.add_frame, "Name:")
        self.create_label_entry(self.add_frame, "Membership ID:")
        self.create_label_entry(self.add_frame, "Department:")
        self.create_label_entry(self.add_frame, "Program:")
        self.create_label_entry(self.add_frame, "Photo:")

        # Submit button
        self.submit_button = tk.Button(self.add_frame, text="Submit", command=self.submit_member, bg="black", fg="white", bd=0, highlightthickness=0, font=("Helvetica", 14))
        self.submit_button.pack(pady=10)

        # Back button
        self.back_button = tk.Button(self.add_frame, text="Back", command=self.go_back, bg="black", fg="white", bd=0, highlightthickness=0, font=("Helvetica", 14))
        self.back_button.pack(pady=10)

    def create_label_entry(self, frame, label_text):
        container = tk.Frame(frame)
        container.pack(fill=tk.X, pady=5)

        tk.Label(container, text=label_text, width=15, anchor='w', font=("Helvetica", 14)).pack(side=tk.LEFT)
        entry = tk.Entry(container, font=("Helvetica", 14))
        entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

        setattr(self, label_text.split(":")[0].lower() + "_entry", entry)

    def create_Add_members_frame(self):
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
        self.csv_path_entry.delete(0, tk.END)
        csv_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        self.csv_path_entry.insert(0, csv_path)

    def browse_photo_folder(self):
        self.photo_folder_path_entry.delete(0, tk.END)
        photo_folder_path = filedialog.askdirectory()
        self.photo_folder_path_entry.insert(0, photo_folder_path)

    def submit_member(self):
        name = self.name_entry.get()
        membership_id = self.membership_id_entry.get()
        department = self.department_entry.get()
        program = self.program_entry.get()
        photo = self.photo_entry.get()

        if not all([name, membership_id, department, program, photo]):
            messagebox.showerror("Input Error", "All fields are required.")
            return

        messagebox.showinfo("Member Added", f"Name: {name}\nMembership ID: {membership_id}\nDepartment: {department}\nProgram: {program}\nPhoto: {photo}")

    def submit_bulk_members(self):
        csv_path = self.csv_path_entry.get()
        photo_folder_path = self.photo_folder_path_entry.get()

        if not all([csv_path, photo_folder_path]):
            messagebox.showerror("Input Error", "Both CSV file path and photo folder path are required.")
            return

        try:
            df = pd.read_csv(csv_path)
            for index, row in df.iterrows():
                name = row['name']
                membership_id = row['membership_id']
                department = row['department']
                program = row['program']
                photo_path = os.path.join(photo_folder_path, row['photo'])

                if not os.path.exists(photo_path):
                    photo_path = None

                print(f"Processed member: {name}, {membership_id}, {department}, {program}, {photo_path}")

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
    root.geometry("800x600")  # Set to a larger size to occupy full screen

    class LibrarySelectionInterface:
        def __init__(self, root, login_interface):
            self.root = root

        def create_library_selection_frame(self):
            pass  # Implement the necessary interface creation here

    class LoginInterface:
        def __init__(self, root):
            self.root = root

    login_interface = LoginInterface(root)
    app = LibrarySelectionInterface(root, login_interface)
    no_of = "single"  # Change to "bulk" for bulk addition
    member_type = "UG"  # Example member type
    b = add_member(root, app, no_of, member_type)
    root.mainloop()
