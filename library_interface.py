import tkinter as tk
from tkinter import messagebox
import time
from PIL import Image, ImageTk
import psycopg2
from report_generation import ReportGeneration

class LibraryInterface:
    def __init__(self, root, library_name, previous_interface):
        self.root = root
        self.library_name = library_name
        self.previous_interface = previous_interface
        self.create_library_interface()

    def create_library_interface(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.library_frame = tk.Frame(self.root)
        self.library_frame.grid(sticky='nsew')

        for i in range(8):  # Increase the number of rows to 8
            self.library_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            self.library_frame.grid_columnconfigure(j, weight=1)

        # Load and display the selected library image
        if self.library_name == 'Nila':
            file = 'images/nila_library.png'
        elif self.library_name == 'Sahyadri':
            file = 'images/sahyadri_library.png'
        self.library_image = Image.open(file)
        self.library_image = self.library_image.resize((1500, 110), Image.LANCZOS)
        self.library_image = ImageTk.PhotoImage(self.library_image)

        tk.Label(self.library_frame, image=self.library_image).grid(row=0, column=0, columnspan=4, sticky='ew')

        self.current_time_label = tk.Label(self.library_frame, font=("Helvetica", 16))
        self.current_time_label.grid(row=1, column=2, columnspan=2, padx=10, sticky='ne')
        self.update_time()

        self.people_count_label = tk.Label(self.library_frame, text="No. of people in the library: 0", font=("Helvetica", 16))
        self.people_count_label.grid(row=1, column=0, columnspan=2, padx=10, sticky='nw')
        self.update_people_count()

        self.scan_label = tk.Label(self.library_frame, text="Scan Here", font=("Helvetica", 16))
        self.scan_label.grid(row=2, column=0, columnspan=4, pady=10, sticky='ew')

        # Load and display the GIF image
        self.gif_image = Image.open('images/scan_animation.gif')
        self.gif_frames = []
        try:
            while True:
                self.gif_frames.append(ImageTk.PhotoImage(self.gif_image.copy()))
                self.gif_image.seek(len(self.gif_frames))  # Move to the next frame
        except EOFError:
            pass  # End of sequence

        self.gif_label = tk.Label(self.library_frame)
        self.gif_label.grid(row=3, column=0, columnspan=4, pady=10, sticky='ew')
        self.animate_gif(0)

        self.scan_entry = tk.Entry(self.library_frame, font=("Helvetica", 16))
        self.scan_entry.grid(row=4, column=0, columnspan=4, pady=10, sticky='ew')

        self.search_button = tk.Button(self.library_frame, text="Search ID", command=lambda: self.search_id(self.library_name), font=("Helvetica", 16))
        self.search_button.grid(row=5, column=0, columnspan=4, pady=5, sticky='ew')

        self.person_details_frame = tk.Frame(self.library_frame)
        self.person_details_frame.grid(row=6, column=0, columnspan=4, pady=10, sticky='ew')
        self.person_photo_label = tk.Label(self.person_details_frame)
        self.person_photo_label.grid(row=0, column=0, rowspan=4, padx=10)
        self.person_details_labels = []

        tk.Button(self.library_frame, text="Generate Report", command=self.generate_report, font=("Helvetica", 16)).grid(row=7, column=0, pady=10, padx=10, sticky='sw')
        tk.Button(self.library_frame, text="Back", command=self.go_back, font=("Helvetica", 16)).grid(row=7, column=3, pady=10, padx=10, sticky='se')

    def animate_gif(self, frame_index):
        if frame_index<len(self.gif_frames):
            frame = self.gif_frames[frame_index]
            if self.gif_label.winfo_exists():
                
                self.gif_label.config(image=frame)
                self.root.after(100, self.animate_gif, (frame_index + 1) % len(self.gif_frames))

            else:
                pass
    def update_time(self):
        current_time = time.strftime('%H:%M:%S')
        current_date = time.strftime('%Y-%m-%d')
        if self.current_time_label.winfo_exists():
            
            self.current_time_label.config(text=f"Current Time: {current_time}")

            if current_time == '00:00:00' or self.check_pending_checkouts(current_date):
                self.handle_midnight_checkout(current_date)

        self.root.after(1000, self.update_time)

    def check_pending_checkouts(self, current_date):
        conn = psycopg2.connect(
            dbname="library_dbms",
            user="postgres",
            password="S@i*iran2004",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        cursor.execute('''
            SELECT COUNT(*) FROM log 
            WHERE checkout IS NULL 
            AND date < %s
        ''', (current_date,))
        count = cursor.fetchone()[0]

        conn.close()

        return count > 0

    def handle_midnight_checkout(self, current_date):
        conn = psycopg2.connect(
            dbname="library_dbms",
            user="postgres",
            password="S@i*iran2004",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE log 
            SET checkout = '24:00:00' 
            WHERE checkout IS NULL 
            AND date < %s
        ''', (current_date,))
        conn.commit()
        conn.close()

        self.update_people_count()

    def search_id(self, library_name):
        person_id = self.scan_entry.get()
        conn = psycopg2.connect(
            dbname="library_dbms",
            user="postgres",
            password="S@i*iran2004",
            host="localhost",
            port="5432"
        )
        
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM student WHERE id=%s', (person_id,))
        student = cursor.fetchone()

        cursor.execute('SELECT * FROM faculty WHERE id=%s', (person_id,))
        faculty = cursor.fetchone()
        if student:
            id = student[0]
            name = student[1]
            program = student[2]
            department = student[3]
            self.display_person_details(student, person_type="student")
            
            self.log_entry(id, name, program, department, library_name, "student")
        elif faculty:
            id = faculty[0]
            name = faculty[1]
            department = faculty[2]
            self.display_person_details(faculty, person_type="faculty")
            
            self.log_entry(id, name, None, department, library_name, "faculty")
        else:
            messagebox.showerror("Error", "ID not found")

        conn.close()
        self.scan_entry.delete(0, tk.END)

    def display_person_details(self, person, person_type):
        id, name, *details = person
        if person_type == "student":
            program, department = details[:2]  # Ensure we only take the first two details
        else:
            department, = details[:1]  # Ensure we only take the first detail
            program = None

        # Load person photo or default photo
        photo_path = f'images/{id}.png'  # Assuming photos are stored with their IDs as filenames
        try:
            person_photo = Image.open(photo_path)
        except FileNotFoundError:
            person_photo = Image.open('images/photo.jpg')  # Default photo if not found
        person_photo = person_photo.resize((150, 200), Image.LANCZOS)
        person_photo = ImageTk.PhotoImage(person_photo)
        self.person_photo_label.config(image=person_photo)
        self.person_photo_label.image = person_photo

        # Clear previous details
        for label in self.person_details_labels:
            label.destroy()
        self.person_details_labels.clear()

        # Hide initial elements
        self.scan_label.grid_forget()
        self.gif_label.grid_forget()
        self.scan_entry.grid_forget()
        self.search_button.grid_forget()

        # Display new details
        details_texts = [
            f"Name: {name}",
            f"ID: {id}",
            f"Program: {program}" if program else None,
            f"Department: {department}"
        ]
        for i, text in enumerate(filter(None, details_texts)):
            label = tk.Label(self.person_details_frame, text=text, font=("Helvetica", 16))
            label.grid(row=i, column=1, sticky='w')
            self.person_details_labels.append(label)

        self.root.after(5000, self.reset_scan_page)

    def reset_scan_page(self):
        self.person_photo_label.config(image='')
        for label in self.person_details_labels:
            label.destroy()
        self.person_details_labels.clear()
        
        self.scan_label.grid(row=2, column=0, columnspan=4, pady=10, sticky='ew')
        self.gif_label.grid(row=3, column=0, columnspan=4, pady=10, sticky='ew')
        self.scan_entry.grid(row=4, column=0, columnspan=4, pady=10, sticky='ew')
        self.search_button.grid(row=5, column=0, columnspan=4, pady=5, sticky='ew')

    def log_entry(self, id, name, program, department, library_name, person_type):
        conn = psycopg2.connect(
            dbname="library_dbms",
            user="postgres",
            password="S@i*iran2004",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM log WHERE id=%s AND type=%s AND checkout IS NULL', (id, person_type))
        log = cursor.fetchone()

        if log:
            cursor.execute('UPDATE log SET checkout=%s WHERE id=%s AND checkout IS NULL', (time.strftime('%H:%M'), id))
        else:
            cursor.execute('INSERT INTO log (id, name, type, program, department, date, library_name, checkin) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (id, name, person_type, program, department, time.strftime('%Y-%m-%d'), library_name, time.strftime('%H:%M')))

        conn.commit()
        conn.close()

        self.update_people_count()

    def update_people_count(self):
        conn = psycopg2.connect(
            dbname="library_dbms",
            user="postgres",
            password="S@i*iran2004",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM log WHERE checkout IS NULL AND library_name =%s',(self.library_name,))
        count = cursor.fetchone()[0]

        conn.close()
        if self.people_count_label.winfo_exists():
            self.people_count_label.config(text=f"No. of people in the library: {count}")

    def generate_report(self):
        ReportGeneration(self.root, self.library_name, self)

    def go_back(self):
        self.library_frame.destroy()
        self.previous_interface.create_library_selection_frame()

if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-fullscreen', True)  # Make the window fullscreen

    app = LibraryInterface(root, "Nila Library", None)
    root.mainloop()
