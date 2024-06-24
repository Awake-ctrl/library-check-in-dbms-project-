# press date wise button in library_dbms_pg.py
# it opens this report.py
# then 
# file =open_excel(log_data.xlsx)
# open a interface ask the from date and to date ,ask the library name  :
#     then open the file check the data from data and to date :
#         check the library name 
#         if it is sahyadri :
#             check only campus=sahyadri 
#         if it is nila:
#             check only campus= nila
#         if both :
#             check campus =nila|sahyadri
#         display three picharts:
#             first one take type details from file and make pichart and name it as type of Person 
#             second one take program details from file and make pichart and name it as program of person 
#             third one take department details from file and make pichart and name it as department of person 
# down there should a download button :
#     export the displayed data into a pdf form and name it as date wise report 
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.utils import ImageReader
import datetime

class ReportGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Report Generator")
        self.create_interface()
        self.adjust_to_screen_size()

    def create_interface(self):
        self.frame = tk.Frame(self.root)
        self.frame.grid(sticky='nsew')
        
        tk.Label(self.frame, text="From Date (YYYY-MM-DD)", font=("Helvetica", 14)).grid(row=0, column=0, pady=10)
        self.from_date_entry = tk.Entry(self.frame, font=("Helvetica", 14))
        self.from_date_entry.grid(row=0, column=1, pady=10)
        
        tk.Label(self.frame, text="To Date (YYYY-MM-DD)", font=("Helvetica", 14)).grid(row=1, column=0, pady=10)
        self.to_date_entry = tk.Entry(self.frame, font=("Helvetica", 14))
        self.to_date_entry.grid(row=1, column=1, pady=10)
        
        tk.Label(self.frame, text="Library Name", font=("Helvetica", 14)).grid(row=2, column=0, pady=10)
        self.library_name_var = tk.StringVar()
        self.library_name_option = tk.OptionMenu(self.frame, self.library_name_var, "Nila", "Sahyadri", "Both")
        self.library_name_option.grid(row=2, column=1, pady=10)

        self.data_display = tk.Text(self.frame, font=("Helvetica", 12), height=10, width=80)
        self.data_display.grid(row=3, column=0, columnspan=2, pady=10)
        
        tk.Button(self.frame, text="Generate Report", command=self.generate_report, font=("Helvetica", 14)).grid(row=4, column=0, columnspan=2, pady=10)
        
        tk.Button(self.frame, text="Back", command=self.root.destroy, font=("Helvetica", 14)).grid(row=5, column=0, columnspan=2, pady=10)
        
    def generate_report(self):
        from_date = self.from_date_entry.get()
        to_date = self.to_date_entry.get()
        library_name = self.library_name_var.get()
        
        try:
            # Validate date inputs
            from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')
            to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d')
            
            if from_date > to_date:
                messagebox.showerror("Error", "From Date cannot be after To Date")
                return

            # Load data from Excel
            file_path = "log_data.xlsx"
            data = pd.read_excel(file_path)
            
            # Filter data based on date range and library name
            data['date'] = pd.to_datetime(data['date'])
            data = data[(data['date'] >= from_date) & (data['date'] <= to_date)]
            
            if library_name == "Nila":
                data = data[data['library_name'] == "Nila"]
            elif library_name == "Sahyadri":
                data = data[data['library_name'] == "Sahyadri"]
            # else: keep both
            
            if data.empty:
                self.data_display.delete('1.0', tk.END)
                self.data_display.insert(tk.END, "No data found for the given criteria.")
                return

            self.display_data(data)
            self.create_pie_charts(data)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def display_data(self, data):
        self.data_display.delete('1.0', tk.END)
        self.data_display.insert(tk.END, data.to_string(index=False))

    def create_pie_charts(self, data):
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        
        # Pie chart for type of person
        type_counts = data['type'].value_counts()
        axes[0].pie(type_counts, labels=type_counts.index, autopct='%1.1f%%')
        axes[0].set_title('Type of Person')
        
        # Pie chart for program
        program_counts = data['program'].value_counts()
        axes[1].pie(program_counts, labels=program_counts.index, autopct='%1.1f%%')
        axes[1].set_title('Program of Person')
        
        # Pie chart for department
        department_counts = data['department'].value_counts()
        axes[2].pie(department_counts, labels=department_counts.index, autopct='%1.1f%%')
        axes[2].set_title('Department of Person')
        
        plt.tight_layout()
        
        # Save the pie charts to a BytesIO object
        pie_charts = BytesIO()
        plt.savefig(pie_charts, format='png')
        plt.close(fig)
        pie_charts.seek(0)
        
        # Display and save PDF report
        self.display_and_save_pdf(data, pie_charts)

    def display_and_save_pdf(self, data, pie_charts):
        # Ask the user where to save the PDF file
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        pdf_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", 
            filetypes=[("PDF files", "*.pdf")], 
            title="Save report as", 
            initialfile=f"date_wise_report_{current_date}.pdf"
        )
        
        if pdf_path:
            c = canvas.Canvas(pdf_path, pagesize=letter)
            width, height = letter
            
            c.drawString(30, height - 30, "Library Log Report")
            
            data_text = data.to_string(index=False)
            text_object = c.beginText(30, height - 50)
            text_object.setFont("Helvetica", 10)
            text_object.textLines(data_text)
            c.drawText(text_object)
            
            # Add pie charts
            pie_charts_reader = ImageReader(pie_charts)
            c.drawImage(pie_charts_reader, 30, height - 450, width - 60, 300)
            
            c.showPage()
            c.save()
            messagebox.showinfo("Info", f"Report saved successfully as {pdf_path}")

    def adjust_to_screen_size(self):
        self.root.update_idletasks()
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.root.geometry(f"{width}x{height}")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = ReportGenerator(root)
    root.mainloop()
