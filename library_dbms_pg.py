import tkinter as tk
from tkinter import messagebox
import psycopg2
import time
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import subprocess

class LibraryDBMS:
    def __init__(self, root):
        self.root = root
        self.root.title("INDIAN INSTITUTE OF TECHNOLOGY PALAKKAD")
        self.root.state('zoomed')  # Make the window full screen
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        
        self.create_login_frame()
    
    def create_login_frame(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.grid(sticky='nsew')
        
        tk.Label(self.login_frame, text="INDIAN INSTITUTE OF TECHNOLOGY PALAKKAD", font=("Helvetica", 24)).grid(row=0, column=0, columnspan=2, pady=10)
        
        tk.Label(self.login_frame, text="Username", font=("Helvetica", 16)).grid(row=1, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(self.login_frame, font=("Helvetica", 16))
        self.username_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(self.login_frame, text="Password", font=("Helvetica", 16)).grid(row=2, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(self.login_frame, show="*", font=("Helvetica", 16))
        self.password_entry.grid(row=2, column=1, padx=10, pady=10)
        
        self.show_password_var = tk.IntVar()
        tk.Checkbutton(self.login_frame, text="Show Password", variable=self.show_password_var, command=self.toggle_password, font=("Helvetica", 16)).grid(row=3, column=0, columnspan=2)
        
        tk.Button(self.login_frame, text="Login", command=self.login, font=("Helvetica", 16)).grid(row=4, column=0, columnspan=2, pady=10)
        
    def toggle_password(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        conn = psycopg2.connect(
            dbname="library_dbms",
            user="postgres",
            password="S@i*iran2004",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username=%s AND password=%s', (username, password))
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            self.login_frame.destroy()
            self.create_library_selection_frame()
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def create_library_selection_frame(self):
        self.library_selection_frame = tk.Frame(self.root)
        self.library_selection_frame.grid(sticky='nsew')
        
        tk.Label(self.library_selection_frame, text="INDIAN INSTITUTE OF TECHNOLOGY PALAKKAD", font=("Helvetica", 24)).grid(row=0, column=0, columnspan=2, pady=10)
        
        tk.Button(self.library_selection_frame, text="Nila Library", command=self.open_nila_library, font=("Helvetica", 16)).grid(row=1, column=0, pady=5)
        tk.Button(self.library_selection_frame, text="Sahyadri Library", command=self.open_sahyadri_library, font=("Helvetica", 16)).grid(row=1, column=1, pady=5)
    
    def open_nila_library(self):
        self.library_selection_frame.destroy()
        self.create_library_interface("Nila Library")
    
    def open_sahyadri_library(self):
        self.library_selection_frame.destroy()
        self.create_library_interface("Sahyadri Library")
    
    def create_library_interface(self, library_name):
        self.library_frame = tk.Frame(self.root)
        self.library_frame.grid(sticky='nsew')

        tk.Label(self.library_frame, text="INDIAN INSTITUTE OF TECHNOLOGY PALAKKAD", font=("Helvetica", 24)).grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(self.library_frame, text=library_name, font=("Helvetica", 20)).grid(row=1, column=0, columnspan=2, pady=10)

        self.current_time_label = tk.Label(self.library_frame, font=("Helvetica", 16))
        self.current_time_label.grid(row=2, column=0, columnspan=2, pady=10)
        self.update_time()

        self.people_count_label = tk.Label(self.library_frame, text="No. of people in the library: 0", font=("Helvetica", 16))
        self.people_count_label.grid(row=3, column=0, columnspan=2, pady=10)

        self.scan_label = tk.Label(self.library_frame, text="Scan Here", font=("Helvetica", 16))
        
        self.scan_label.grid(row=4, column=0, columnspan=2, pady=10)

        self.scan_entry = tk.Entry(self.library_frame, font=("Helvetica", 16))
        self.scan_entry.grid(row=5, column=0, columnspan=2, pady=10)

        # Button to search the ID in the database
        self.search_button = tk.Button(self.library_frame, text="Search ID", command=lambda: self.search_id(library_name), font=("Helvetica", 16))
        self.search_button.grid(row=6, column=0, columnspan=2, pady=5)

        self.person_details_label = tk.Label(self.library_frame, text="", font=("Helvetica", 16))
        self.person_details_label.grid(row=7, column=0, columnspan=2, pady=10)

        tk.Button(self.library_frame, text="Generate Report", command=self.generate_report, font=("Helvetica", 16)).grid(row=8, column=0, columnspan=2, pady=10)

    def update_time(self):
        current_time = time.strftime('%H:%M:%S')
        self.current_time_label.config(text=f"Current Time: {current_time}")
        self.root.after(1000, self.update_time)

    def search_id(self,library_name):
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
            self.display_person_details(f"Name: {student[1]}, ID: {student[0]}, Program: {student[2]}, Department: {student[3]}")
            self.log_entry(id, name, program, department, library_name,"student")
        elif faculty:
            id = faculty[0]
            name = faculty[1]
            department = faculty[2]
            self.display_person_details(f"Name: {faculty[1]}, ID: {faculty[0]}, Department: {faculty[2]}")
            self.log_entry(id, name, None, department,library_name, "faculty")
        else:
            messagebox.showerror("Error", "ID not found")

        conn.close()
        self.scan_entry.delete(0, tk.END)

    def display_person_details(self, details):
        self.scan_label.grid_forget()
        self.scan_entry.grid_forget()
        self.search_button.grid_forget()

        self.person_details_label.config(text=details)
        
        self.root.after(5000, self.reset_scan_page)

    def reset_scan_page(self):
        self.person_details_label.config(text="")
        
        self.scan_label.grid(row=4, column=0, columnspan=2, pady=10)
        self.scan_entry.grid(row=5, column=0, columnspan=2, pady=10)
        self.search_button.grid(row=6, column=0, columnspan=2, pady=5)

    def log_entry(self, id, name, program, department,library_name, person_type):
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
            cursor.execute('UPDATE log SET checkout=%s WHERE id=%s AND checkout IS NULL', (time.strftime('%H:%M:%S'), id))
            self.update_people_count(-1)
        else:
            cursor.execute('INSERT INTO log (id, name, type, program, department, date,library_name, checkin) VALUES (%s, %s, %s, %s, %s,%s, %s, %s)', (id, name, person_type, program, department, time.strftime('%Y-%m-%d'), library_name,time.strftime('%H:%M:%S')))
            self.update_people_count(1)

        conn.commit()
        conn.close()

    def update_people_count(self, change):
        current_count = int(self.people_count_label.cget("text").split(": ")[1])
        new_count = current_count + change
        self.people_count_label.config(text=f"No. of people in the library: {new_count}")

    def generate_report(self):
        report_window = tk.Toplevel(self.root)
        report_window.title("Generate Report")
        report_window.geometry("400x300")

        tk.Label(report_window, text="Generate Report for:", font=("Helvetica", 16)).pack(pady=10)

        tk.Button(report_window, text="Date-wise", command=self.date_wise, font=("Helvetica", 16)).pack(pady=5)
        tk.Button(report_window, text="Membership Category-wise", command=lambda: self.create_report("category"), font=("Helvetica", 16)).pack(pady=5)
        tk.Button(report_window, text="User-wise", command=lambda: self.create_report("user"), font=("Helvetica", 16)).pack(pady=5)
    def date_wise(self):
        # Run the other Python script in a new process
        subprocess.Popen(["python", "date_wise_report.py"])
    def create_report(self, report_type):
        report_window = tk.Toplevel(self.root)
        report_window.title(f"{report_type.capitalize()} Report")
        report_window.geometry("600x400")

        conn = psycopg2.connect(
            dbname="library_dbms",
            user="postgres",
            password="S@i*iran2004",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        if report_type == "date":
            cursor.execute('SELECT * FROM log ORDER BY checkin')
        elif report_type == "category":
            cursor.execute('SELECT type, COUNT(*) FROM log GROUP BY type')
        elif report_type == "user":
            cursor.execute('SELECT id, COUNT(*) FROM log GROUP BY id')

        logs = cursor.fetchall()

        report_text = tk.Text(report_window, font=("Helvetica", 12))
        report_text.pack(fill='both', expand=True)

        report_text.insert(tk.END, f"{report_type.capitalize()} Report\n\n")

        for log in logs:
            report_text.insert(tk.END, f"{log}\n")

        conn.close()

        tk.Button(report_window, text="Export as PDF", command=lambda: self.export_as_pdf(report_type, logs), font=("Helvetica", 16)).pack(pady=10)
        tk.Button(report_window, text="Send via Email", command=lambda: self.send_via_email(report_type), font=("Helvetica", 16)).pack(pady=10)

    def export_as_pdf(self, report_type, logs):
        pdf_path = f"{report_type}_report.pdf"
        pdf = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter

        pdf.setFont("Helvetica", 12)
        y = height - 40
        pdf.drawString(30, y, f"{report_type.capitalize()} Report")
        y -= 20

        for log in logs:
            pdf.drawString(30, y, str(log))
            y -= 20
            if y < 40:
                pdf.showPage()
                y = height - 40
                pdf.setFont("Helvetica", 12)

        pdf.save()
        messagebox.showinfo("Success", f"Report saved as {pdf_path}")

    def send_via_email(self, report_type):
        pdf_path = f"{report_type}_report.pdf"
        self.export_as_pdf(report_type, [])

        sender_email = "kallepallysaikiran21@gmail.com"
        receiver_email = "112201044@smail.iitpkd.ac.in"
        password = "S@i*iran2004"

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = f"{report_type.capitalize()} Report"

        part = MIMEBase("application", "octet-stream")
        part.set_payload(open(pdf_path, "rb").read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={pdf_path}")
        msg.attach(part)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())

        messagebox.showinfo("Success", "Email sent successfully")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryDBMS(root)
    root.mainloop()


