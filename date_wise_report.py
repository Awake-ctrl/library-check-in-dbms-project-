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
import psycopg2
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.utils import ImageReader
import datetime
from tkcalendar import DateEntry

class ReportGenerator:
    def __init__(self, root):
        self.root = root
        self.previous_window = None # To store the previous window
        self.DATA=""
        self.membership_value=False
        self.Membership_type=""
        # self.animate_gif()
        # self.update_time()
        self.create_interface()

    def create_interface(self):
        self.frame = tk.Frame(self.root)
        self.frame.grid(sticky='nsew')
        tk.Label(self.frame, text="Report ", font=("Helvetica", 24)).grid(row=0, column=1, columnspan=2, pady=10,sticky="ew")
        tk.Label(self.frame, text="       ", font=("Helvetica", 24)).grid(row=1, column=1, columnspan=2, pady=10,sticky="ew")
        
        #username 
        tk.Label(self.frame, text="User Name", font=("Helvetica", 14)).grid(row=2, column=0, pady=10,sticky="w")
        self.username = tk.Entry(self.frame, font=("Helvetica", 14))
        self.username.grid(row=2, column=1, pady=10,sticky="w")
        
        #password
        tk.Label(self.frame, text="Password", font=("Helvetica", 14)).grid(row=2, column=2, pady=10,sticky="w")
        self.password = tk.Entry(self.frame, show="*",font=("Helvetica", 14))
        self.password.grid(row=2, column=3, pady=10,sticky="w")
        self.show_password_var = tk.IntVar()
        tk.Checkbutton(self.frame, text="Show", variable=self.show_password_var, command=self.toggle_password, font=("Helvetica", 16)).grid(row=2, column=5, columnspan=2, pady=10)
        
        #from date
        tk.Label(self.frame, text="From Date (DD-MM-YYYY)", font=("Helvetica", 14)).grid(row=3, column=0, pady=10,sticky="w")
        self.from_date_entry = DateEntry(self.frame, date_pattern='dd-mm-yyyy', font=("Helvetica", 14))
        self.from_date_entry.grid(row=3, column=1, pady=10,sticky="w")
        
        #to date
        tk.Label(self.frame, text="To Date (DD-MM-YYYY)", font=("Helvetica", 14)).grid(row=3, column=2, pady=10,sticky="w")
        self.to_date_entry = DateEntry(self.frame, date_pattern='dd-mm-yyyy', font=("Helvetica", 14))
        self.to_date_entry.grid(row=3, column=3, pady=10,sticky="w")
        
        #membership category
        tk.Label(self.frame, text="Membership Category", font=("Helvetica", 14)).grid(row=4, column=0, pady=10,sticky="w")
        self.membership_var = tk.StringVar()
        self.membership_option = tk.OptionMenu(self.frame, self.membership_var, "UG","PG","Research Scholar","Faculty","Staff","External Users","Alumni","Family",  "ALL")
        self.membership_option.grid(row=4, column=1, pady=10,sticky="w")
        
        #library name
        tk.Label(self.frame, text="Library Name", font=("Helvetica", 14)).grid(row=4, column=2, pady=10,sticky="w")
        self.library_name_var = tk.StringVar()
        self.library_name_option = tk.OptionMenu(self.frame, self.library_name_var, "Nila", "Sahyadri", "Both")
        self.library_name_option.grid(row=4, column=3, pady=10,sticky="w")

        #data display
        self.data_display = tk.Text(self.frame, font=("Helvetica", 12), height=25, width=100)
        self.data_display.grid(row=5, column=0, columnspan=2, pady=10,sticky='w')
        
        #report button
        tk.Button(self.frame, text="Generate Report", command=self.generate_report, font=("Helvetica", 14)).grid(row=6, column=0, columnspan=2, pady=10)
        
        tk.Button(self.frame, text="Save", command=lambda : self.create_pie_charts(self.DATA,self.membership_value,self.Membership_type), font=("Helvetica", 14)).grid(row=6, column=1, columnspan=2, pady=10)
        
        #back button
        tk.Button(self.frame, text="Back", command=self.go_back, font=("Helvetica", 14)).grid(row=7, column=0, columnspan=2, pady=10)
        
    def toggle_password(self):
        if self.show_password_var.get():
            self.password.config(show="")
        else:
            self.password.config(show="*")

    def generate_report(self):
        from_date = self.from_date_entry.get_date().strftime('%d-%m-%Y')
        to_date = self.to_date_entry.get_date().strftime('%d-%m-%Y')
        membership_type = self.membership_var.get()
        library_name = self.library_name_var.get()
        username = self.username.get()
        password = self.password.get()
        
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
            try:
                # Validate date inputs
                from_date = datetime.datetime.strptime(from_date, '%d-%m-%Y')
                to_date = datetime.datetime.strptime(to_date, '%d-%m-%Y')
                
                if from_date > to_date:
                    messagebox.showerror("Error", "From Date cannot be after To Date")
                    return

                # Load data from Excel
                file_path = "log_data.xlsx"
                data = pd.read_excel(file_path)
                data.drop(columns=['log_id','checkout'], inplace=True, errors='ignore')
                self.membership_value=False
                # Filter data based on date range and library name
                data['date'] = pd.to_datetime(data['date'])
                data = data[(data['date'] >= from_date) & (data['date'] <= to_date)]
                libraries = ["Nila", "Sahyadri"]
                memberships = ["UG", "PG", "Research Scholar", "Faculty", "Staff", "External Users", "Alumni", "Family"]
                if library_name in libraries:
                    data = data[data['library_name'] == library_name]
                if membership_type in memberships:
                    data = data[data['program'] == membership_type]
                    self.membership_value=True
                
                # else: keep both
                
                if data.empty:
                    self.data_display.delete('1.0', tk.END)
                    self.data_display.insert(tk.END, "No data found for the given criteria.")
                    return
                self.Membership_type=membership_type
                self.display_data(data)
                self.DATA=data
                # self.create_pie_charts(data)
                
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", "Invalid username or password")
        
    

    def display_data(self, data):
        self.data_display.delete('1.0', tk.END)
    
        # Format the data as a string with uniform column widths
        formatted_data = data.to_string(index=False)
        
        # Insert the formatted data into the Text widget
        self.data_display.insert(tk.END, formatted_data)
            
   
    def create_pie_charts(self,data,membership_value,Membership_type):
        try:
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
            self.display_and_save_pdf(data, pie_charts,membership_value,Membership_type)
        except Exception as e:
                messagebox.showerror("saikiran", f"An error occurred: {e}")

    def display_and_save_pdf(self, data, pie_charts,membership_value,Membership_type):
        # Ask the user where to save the PDF file
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        file=f"date_wise_report_{current_date}.pdf"
        if membership_value:
            file=f"{Membership_type}_wise_report_{current_date}.pdf"
        pdf_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", 
            filetypes=[("PDF files", "*.pdf")], 
            title="Save report as", 
            initialfile=file
            
        )
        
        if pdf_path:
            c = canvas.Canvas(pdf_path, pagesize=letter)
            width, height = letter
            
            c.drawString(30, height - 30, "Library Log Report")
                 
            # Split data into chunks to fit on PDF pages
            max_rows_per_page = 50  # Adjust as needed
            chunks = [data[i:i + max_rows_per_page] for i in range(0, len(data), max_rows_per_page)]
            
            for chunk_idx, chunk_data in enumerate(chunks):
                if chunk_idx > 0:
                    c.showPage()  # Start a new page for each chunk after the first
                
                # Add data table
                text_y = height - 50
                text_object = c.beginText(30, text_y)
                text_object.setFont("Helvetica", 10)
                
                # Convert chunk_data to string and add to PDF
                chunk_data_str = chunk_data.to_string(index=False)
                text_object.textLines(chunk_data_str)
                c.drawText(text_object)
                
                # Add pie charts
                if chunk_idx == 0:
                    pie_charts_reader = ImageReader(pie_charts)
                    c.drawImage(pie_charts_reader, 30, height - 450, width - 60, 300)
            
            c.showPage()
            c.save()
            
            messagebox.showinfo("Info", f"Report saved successfully as {pdf_path}")

            # data_text = data.to_string(index=False)
            # text_object = c.beginText(30, height - 50)
            # text_object.setFont("Helvetica", 10)
            # text_object.textLines(data_text)
            # c.drawText(text_object)
            
            # # Add pie charts
            # pie_charts_reader = ImageReader(pie_charts)
            # c.drawImage(pie_charts_reader, 30, height - 450, width - 60, 300)
            
            # c.showPage()
            # c.save()
            # messagebox.showinfo("Info", f"Report saved successfully as {pdf_path}")

    def go_back(self):
        self.root.destroy()
        if self.previous_window:
            
            self.previous_window.deiconify()

    def run(self):
        self.root.attributes('-fullscreen', True)  # Set fullscreen mode
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.mainloop()
    # def animate_gif(self, gif_label, gif_frames, current_frame):
    #     if gif_label.winfo_exists():
    #         frame = gif_frames[current_frame]
    #         gif_label.config(image=frame)
    #         next_frame = (current_frame + 1) % len(gif_frames)
    #         self.gif_task_id = self.root.after(100, self.animate_gif, gif_label, gif_frames, next_frame)

    # def update_time(self):
    #     current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     if self.current_time_label.winfo_exists():
    #         self.current_time_label.config(text=f"Current Time: {current_time}")
    #         self.time_task_id = self.root.after(1000, self.update_time)

if __name__ == "__main__":
    root = tk.Tk()
    app = ReportGenerator(root)
    app.run()
    
