# import os
# import tkinter as tk 
# from PIL import Image,ImageTk 
# from library_selection import LibrarySelectionInterface

# class add_member:
#     def __init__(self,root,previous_interface,no_of) :
#         self.root=root
#         self.previous_interface=previous_interface
#         if no_of=="single":
#             self.create_Add_member_frame()
#         else:
#             self.create_Add_members_frame
#     def create_Add_member_frame(self):
#         self.add_frame=tk.Frame(self.root)
#         self.add_frame.grid(sticky='nsew')
        
#         pass
#     def create_Add_members_frame(self):
#         pass
    
        
        
# if __name__=="__main__":
#     root=tk.Tk()
#     login_interface = LoginInterface(root)
#     app = LibrarySelectionInterface(root, login_interface)
#     no_of="single"
#     b=add_member(root,app,no_of)
#     root.mainloop()
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pandas as pd

class add_member:
    def __init__(self, root, previous_interface, no_of):
        self.root = root
        self.previous_interface = previous_interface
        if no_of == "single":
            self.create_Add_member_frame()
        else:
            self.create_Add_members_frame()

    def create_Add_member_frame(self):
        self.add_frame = tk.Frame(self.root)
        self.add_frame.grid(sticky='nsew')

        tk.Label(self.add_frame, text="Add Member").grid(row=0, columnspan=2)

        tk.Label(self.add_frame, text="Name:").grid(row=1, column=0, sticky=tk.W)
        self.name_entry = tk.Entry(self.add_frame)
        self.name_entry.grid(row=1, column=1)

        tk.Label(self.add_frame, text="Membership ID:").grid(row=2, column=0, sticky=tk.W)
        self.membership_id_entry = tk.Entry(self.add_frame)
        self.membership_id_entry.grid(row=2, column=1)

        tk.Label(self.add_frame, text="Department:").grid(row=3, column=0, sticky=tk.W)
        self.department_entry = tk.Entry(self.add_frame)
        self.department_entry.grid(row=3, column=1)

        tk.Label(self.add_frame, text="Program:").grid(row=4, column=0, sticky=tk.W)
        self.program_entry = tk.Entry(self.add_frame)
        self.program_entry.grid(row=4, column=1)

        tk.Label(self.add_frame, text="Photo:").grid(row=5, column=0, sticky=tk.W)
        self.photo_entry = tk.Entry(self.add_frame)
        self.photo_entry.grid(row=5, column=1)

        self.submit_button = tk.Button(self.add_frame, text="Submit", command=self.submit_member)
        self.submit_button.grid(row=6, columnspan=2)

        self.back_button = tk.Button(self.add_frame, text="Back", command=self.go_back)
        self.back_button.grid(row=7, columnspan=2)

        self.add_frame.pack(expand=True, fill=tk.BOTH)

    def create_Add_members_frame(self):
        self.add_frame = tk.Frame(self.root)
        self.add_frame.grid(sticky='nsew')

        tk.Label(self.add_frame, text="Add Members in Bulk").grid(row=0, columnspan=2)

        tk.Label(self.add_frame, text="CSV File Path:").grid(row=1, column=0, sticky=tk.W)
        self.csv_path_entry = tk.Entry(self.add_frame)
        self.csv_path_entry.grid(row=1, column=1)
        self.csv_browse_button = tk.Button(self.add_frame, text="Browse", command=self.browse_csv)
        self.csv_browse_button.grid(row=1, column=2)

        tk.Label(self.add_frame, text="Photo Folder Path:").grid(row=2, column=0, sticky=tk.W)
        self.photo_folder_path_entry = tk.Entry(self.add_frame)
        self.photo_folder_path_entry.grid(row=2, column=1)
        self.photo_browse_button = tk.Button(self.add_frame, text="Browse", command=self.browse_photo_folder)
        self.photo_browse_button.grid(row=2, column=2)

        self.submit_button = tk.Button(self.add_frame, text="Submit", command=self.submit_bulk_members)
        self.submit_button.grid(row=3, columnspan=3)

        self.back_button = tk.Button(self.add_frame, text="Back", command=self.go_back)
        self.back_button.grid(row=4, columnspan=3)

        self.add_frame.pack(expand=True, fill=tk.BOTH)

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

        # Here you can add code to save the member information to your database or a file
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

                # Here you can add code to save each member information to your database or a file
                print(f"Processed member: {name}, {membership_id}, {department}, {program}, {photo_path}")

            messagebox.showinfo("Bulk Members Added", "All members have been processed.")
        except Exception as e:
            messagebox.showerror("Processing Error", f"An error occurred: {e}")

    def go_back(self):
        self.add_frame.destroy()
        self.previous_interface.root.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Library Management System")
    root.geometry("500x400")

    class LibrarySelectionInterface:
        def __init__(self, root, login_interface):
            self.root = root

    class LoginInterface:
        def __init__(self, root):
            self.root = root

    login_interface = LoginInterface(root)
    app = LibrarySelectionInterface(root, login_interface)
    no_of = "single"  # Change to "bulk" for bulk addition
    b = add_member(root, app, no_of)
    root.mainloop()
