import tkinter as tk
from tkinter import messagebox
import psycopg2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

class ReportInterface:
    def __init__(self, root, report_type, library_name, previous_interface):
        self.root = root
        self.report_type = report_type
        self.library_name = library_name
        self.previous_interface = previous_interface
        self.create_report()

    def create_report(self):
        self.report_frame = tk.Frame(self.root)
        self.report_frame.grid(sticky='nsew')

        tk.Label(self.report_frame, text=f"{self.report_type.capitalize()} Report", font=("Helvetica", 24)).grid(row=0, column=0, columnspan=2, pady=10)

        conn = psycopg2.connect(
            dbname="library_dbms",
            user="postgres",
            password="S@i*iran2004",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        if self.report_type == "date":
            cursor.execute('SELECT * FROM log ORDER BY checkin')
        elif self.report_type == "category":
            cursor.execute('SELECT type, COUNT(*) FROM log GROUP BY type')
        elif self.report_type == "user":
            cursor.execute('SELECT id, COUNT(*) FROM log GROUP BY id')

        logs = cursor.fetchall()

        report_text = tk.Text(self.report_frame, font=("Helvetica", 12))
        report_text.grid(row=1, column=0, columnspan=2, pady=10, padx=10)
        report_text.insert(tk.END, f"{self.report_type.capitalize()} Report\n\n")

        for log in logs:
            report_text.insert(tk.END, f"{log}\n")

        conn.close()

        tk.Button(self.report_frame, text="Export as PDF", command=lambda: self.export_as_pdf(logs), font=("Helvetica", 16)).grid(row=2, column=0, pady=10)
        tk.Button(self.report_frame, text="Send via Email", command=lambda: self.send_via_email(logs), font=("Helvetica", 16)).grid(row=2, column=1, pady=10)
        tk.Button(self.report_frame, text="Back", command=self.go_back, font=("Helvetica", 16)).grid(row=3, column=0, columnspan=2, pady=10)

    def export_as_pdf(self, logs):
        pdf_path = f"{self.report_type}_report.pdf"
        pdf = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter

        pdf.setFont("Helvetica", 12)
        y = height - 40
        pdf.drawString(30, y, f"{self.report_type.capitalize()} Report")
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

    def send_via_email(self, logs):
        pdf_path = f"{self.report_type}_report.pdf"
        self.export_as_pdf(logs)

        sender_email = "kallepallysaikiran21@gmail.com"
        receiver_email = "112201044@smail.iitpkd.ac.in"
        password = "S@i*iran2004"

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = f"{self.report_type.capitalize()} Report"

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

    def go_back(self):
        self.report_frame.destroy()
        self.previous_interface.create_report_frame()
