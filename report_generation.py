import tkinter as tk
import psycopg2
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import subprocess
from report_interface import ReportInterface



class ReportGeneration:
    def __init__(self, root, library_name, previous_interface):
        self.root = root
        self.library_name = library_name
        self.previous_interface = previous_interface
        self.create_report_frame()

    def create_report_frame(self):
        self.report_frame = tk.Frame(self.root)
        self.report_frame.grid(sticky='nsew')

        tk.Label(self.report_frame, text="               ", font=("Helvetica", 24)).grid(row=1, column=3, columnspan=2, pady=10)

        tk.Button(self.report_frame, text="Date&category_wise", command=self.date_wise, font=("Helvetica", 16)).grid(row=1, column=0, pady=5)
        # tk.Button(self.report_frame, text="Category-wise", command=lambda: self.category_wise_report("category"), font=("Helvetica", 16)).grid(row=1, column=1, pady=5)
        tk.Button(self.report_frame, text="User-wise", command=lambda: self.user_wise_report("user"), font=("Helvetica", 16)).grid(row=1, column=2, pady=5)
        
        tk.Button(self.report_frame, text="Back", command=self.go_back, font=("Helvetica", 16)).grid(row=1, column=4, pady=5)
    def date_wise(self):
        # Run the other Python script in a new process
        try:
            subprocess.run(["python", "pgadminto_excellog.py"], check=True)
            print("hello new excel")
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
        subprocess.Popen(["python", "date_wise_report.py"])
    # def date_wise_report(self):
    #     self.report_frame.destroy()
    #     ReportInterface(self.root, "date", self.library_name, self)

    # def category_wise_report(self, report_type):
    #     self.report_frame.destroy()
    #     ReportInterface(self.root, "category", self.library_name, self)

    def user_wise_report(self, report_type):
        try:
            subprocess.run(["python","pgadminto_excellog.py"],check=True)
            print("hello new excel")
        except subprocess.CalledProcessError as e:
            print(f"Error:{e}")
        subprocess.Popen(["python","user_wise_report.py"])
        # self.report_frame.destroy()
        # ReportInterface(self.root, "user", self.library_name, self)

    def go_back(self):
        self.report_frame.destroy()
        self.previous_interface.create_library_interface(self.library_name)
