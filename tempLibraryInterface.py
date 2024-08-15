import tkinter as tk
import os
import sys
import pandas as pd
from tkinter import messagebox
import time
from datetime import datetime
from PIL import Image, ImageTk
import psycopg2
# from report_generation import ReportGeneration
import subprocess
from date_wise_report import ReportGenerator1
from user_wise_report import ReportGenerator2

class LibraryInterface:
    def __init__(self, root, library_name, previous_interface):
        self.root = root
        self.library_name = library_name
        self.previous_interface = previous_interface
        self.people_count_label=""
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
        file=""
        # Load and display the selected library image
        if self.library_name == 'Nila':
            # file = 'images/nila_library.png'
            file = os.path.join("images", "nila_library.png")
            print(file)
            
        elif self.library_name == 'Sahyadri':
            # file = 'images/sahyadri_library.png'
            file = os.path.join("images", "sahyadri_library.png")
            print(file)
        # self.library_image = Image.open(file)
        # self.library_image = self.library_image.resize((1500, 110), Image.LANCZOS)
        # self.library_image = ImageTk.PhotoImage(self.library_image)

        # tk.Label(self.library_frame, image=self.library_image).grid(row=0, column=0, columnspan=4, sticky='ew')

        self.current_time_label = tk.Label(self.library_frame, font=("Poppins", 16))
        self.current_time_label.grid(row=1, column=2, columnspan=2, padx=10, sticky='ne')
        self.update_time()

        self.people_count_label = tk.Label(self.library_frame, text="No. of people in the library: 0", font=("Poppins", 16))
        self.people_count_label.grid(row=1, column=0, columnspan=2, padx=10, sticky='nw')
        self.update_people_count(self.people_count_label)

        self.scan_label = tk.Label(self.library_frame, text="Scan Here", font=("Poppins", 16))
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

        self.scan_entry = tk.Entry(self.library_frame, font=("Poppins", 16))
        self.scan_entry.grid(row=4, column=0, columnspan=4, pady=10, sticky='ew')

        self.search_button = tk.Button(self.library_frame, text="Search ID", command=lambda: self.search_id(self.library_name), font=("Poppins", 16))
        self.search_button.grid(row=5, column=0, columnspan=4, pady=5, sticky='ew')

        self.person_details_frame = tk.Frame(self.library_frame)
        self.person_details_frame.grid(row=3, column=0, columnspan=4, pady=10, sticky='ew')
        self.person_photo_label = tk.Label(self.person_details_frame)
        self.person_photo_label.grid(row=0, column=0, rowspan=4, padx=10)
        self.person_details_labels = []

        self.generate_button=tk.Button(self.library_frame, text="Generate Report", command=self.generate_report, font=("Poppins", 16))
        self.generate_button.grid(row=7, column=0, pady=10, padx=10, sticky='sw')
        tk.Label(self.library_frame,text="@credits to kallepally sai kiran ,Ganedi satya harika, Mogili Lavanya",font=("Poppins",11)).grid(row=7, column=1, pady=10, padx=30, sticky='s')
        tk.Button(self.library_frame, text="Back", command=self.go_back, font=("Poppins", 16)).grid(row=7, column=3, pady=10, padx=10, sticky='e')

        self.report_options_frame = tk.Frame(self.library_frame)
        self.report_options_frame.grid(row=7, column=0, columnspan=4, pady=10, sticky='ew')
        self.report_options_frame.grid_remove()  # Hide the report options frame initially

        tk.Button(self.report_options_frame, text="Date & Category-wise", command=self.date_wise, font=("Poppins", 16)).grid(row=0, column=0, pady=5,padx=10)
        tk.Button(self.report_options_frame, text="User-wise", command=self.user_wise_report, font=("Poppins", 16)).grid(row=0, column=1, pady=5,padx=20)

    def animate_gif(self, frame_index):
        if frame_index < len(self.gif_frames):
            frame = self.gif_frames[frame_index]
            if self.gif_label.winfo_exists():
                self.gif_label.config(image=frame)
                self.root.after(100, self.animate_gif, (frame_index + 1) % len(self.gif_frames))

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
            # host="localhost",
            
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

        self.update_people_count(self.people_count_label)

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
            photo_path=student[5]
            
            self.display_person_details(photo_path,student, person_type="student")
            self.log_entry(id, name, program, department, library_name, "student")
            
            
        elif faculty:
            id = faculty[0]
            name = faculty[1]
            department = faculty[2]
            photo_path=faculty[3]
            
            self.display_person_details(photo_path,faculty, person_type="faculty")
            self.log_entry(id, name, None, department, library_name, "faculty")
            
            
        else:
            messagebox.showerror("Error", "ID not found")

        conn.close()
        self.scan_entry.delete(0, tk.END)

    def display_person_details(self, photo_path,person, person_type):
        id, name, *details = person
        if person_type == "student":
            program, department = details[:2]  # Ensure we only take the first two details
        else:
            department, = details[:1]  # Ensure we only take the first detail
            program = None

        # Load person photo or default photo
        if photo_path:
            person_photo = Image.open(photo_path)
        else:
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
            label = tk.Label(self.person_details_frame, text=text, font=("Poppins", 16))
            label.grid(row=i, column=3, sticky='ew')
            self.person_details_labels.append(label)
            
            
            
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
        
        greetings="welcome"

        if log:
            time2=time.strftime('%H:%M:%S')
            time2 = datetime.strptime(time2,'%H:%M:%S' )
            
            time1=str(log[8])
            time1 = datetime.strptime(time1,'%H:%M:%S' )
            print(time1)
            duration=time2-time1
            
            greetings=f"""Thank you visit again
    Your check out is:  {time.strftime('%H:%M:%S')}
    Total time duraton:  {duration} """
    
    
            # cursor.execute('UPDATE log SET checkout=%s WHERE id=%s AND checkout IS NULL', (time.strftime('%H:%M'), id))
        else:
            
            greetings=f""" welcome """
            
            # cursor.execute('INSERT INTO log (id, name, type, program, department, date, library_name, checkin) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (id, name, person_type, program, department, time.strftime('%Y-%m-%d'), library_name, time.strftime('%H:%M')))

        conn.commit()
        conn.close()
        greetings_text=[
            f"{greetings}"
        ]
        z=i+1
        for i,text in enumerate(filter(None,greetings_text)):
            label = tk.Label(self.person_details_frame, text=text, font=("Poppins", 20))
            label.grid(row=i+z, column=3, sticky='ew')
            self.person_details_labels.append(label)

        self.root.after(10000, self.reset_scan_page)

    def reset_scan_page(self):
        self.person_photo_label.config(image='')
        for label in self.person_details_labels:
            label.destroy()
        self.person_details_labels.clear()
        
        self.scan_label.grid(row=2, column=0, columnspan=4, pady=10, sticky='ew')
        self.gif_label.grid(row=3, column=0, columnspan=4, pady=10, sticky='ew')
        self.scan_entry.grid(row=4, column=0, columnspan=4, pady=10, sticky='ew')
        self.search_button.grid(row=5, column=0, columnspan=4, pady=5, sticky='ew')
    def reset_scan_page2(self):
        
        self.generate_button.grid(row=7, column=0, pady=10, padx=10, sticky='sw')
        

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

        self.update_people_count(self.people_count_label)

    def update_people_count(self, people_count_label):
        conn = psycopg2.connect(
            dbname="library_dbms",
            user="postgres",
            password="S@i*iran2004",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM log WHERE checkout IS NULL AND library_name =%s', (self.library_name,))
        count = cursor.fetchone()[0]
        conn.close()
        if self.people_count_label.winfo_exists():
            self.people_count_label.config(text=f"No. of people in the library: {count}")

    def generate_report(self):
        self.generate_button.grid_forget()
        
        
        self.show_report_options()
        # self.root.after(10000, self.reset_scan_page2)
        
        self.root.after(5000, lambda: (self.hide_report_options(), self.reset_scan_page2()))

        
        # self.root.after(10000, self.hide_report_options,self.reset_scan_page2)  # Hide the report options after 10 seconds

    def show_report_options(self):
        
        self.report_options_frame.grid(row=7, column=0, columnspan=4, pady=10, sticky='ew')
        
        

    def hide_report_options(self):
        # self.report_options_frame.grid(row=7, column=0, columnspan=4, pady=10, sticky='ew')
        
        self.report_options_frame.grid_remove()

    def pgadminto_excellog(self):
                
        # Database connection details
        dbname = "library_dbms"
        user = "postgres"
        password = "S@i*iran2004"
        host = "localhost"
        port = "5432"

        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cur = conn.cursor()

        # Create the log table if it doesn't exist
        cur.execute('''
            CREATE TABLE IF NOT EXISTS log (
                log_id SERIAL PRIMARY KEY,
                id VARCHAR(255),
                name VARCHAR(100),
                type VARCHAR(10),
                program VARCHAR(100),
                department VARCHAR(100),
                date DATE,
                library_name VARCHAR(255),
                checkin TIME,
                checkout TIME
            );
        ''')
        conn.commit()

        # Read the data from the server table (assuming the table is named `server_log`)
        cur.execute('SELECT * FROM log;')
        rows = cur.fetchall()

        # Define column names for the dataframe
        columns = ['log_id','id', 'name', 'type', 'program', 'department', 'date', 'library_name','checkin', 'checkout']

        # Convert the data to a pandas DataFrame
        log_df = pd.DataFrame(rows, columns=columns)

        # Write the dataframe to an Excel file
        log_df.to_excel('log_data.xlsx', index=False)

        # Close the connection
        cur.close()
        conn.close()

        
    def date_wise(self):
        self.library_frame.destroy()
        python_executable = sys.executable
        self.pgadminto_excellog()
        
        # try:
        #     subprocess.run([python_executable, "pgadminto_excellog.py"], check=True)
        #     print("1")
        # except subprocess.CalledProcessError as e:
        #     print(f"Error: {e}")
        #     print(f"Error occurred: {e}")
        #     print(f"Return code: {e.returncode}")
        #     print(f"Output: {e.output}")
        #     print(f"Command: {e.cmd}")
        ReportGenerator1(self.root,self)
        # subprocess.Popen(["python", "date_wise_report.py"])

    def user_wise_report(self):
        self.library_frame.destroy()
        python_executable = sys.executable
        self.pgadminto_excellog()
        
        
        # try:
        #     subprocess.run([python_executable, "pgadminto_excellog.py"], check=True)
        #     print("2")
        # except subprocess.CalledProcessError as e:
        #     print(f"Error: {e}")
        #     print(f"Error occurred: {e}")
        #     print(f"Return code: {e.returncode}")
        #     print(f"Output: {e.output}")
        #     print(f"Command: {e.cmd}")
       
        ReportGenerator2(self.root,self)
        # print("it is next step of the calling function")
        # subprocess.Popen(["python", "user_wise_report.py"])

    def go_back(self):
        self.library_frame.destroy()
        self.previous_interface.create_library_selection_frame()

if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-fullscreen', True)  # Make the window fullscreen

    app = LibraryInterface(root, "Nila", None)
    root.mainloop()
