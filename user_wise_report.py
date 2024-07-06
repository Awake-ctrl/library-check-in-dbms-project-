# press date wise button in library_dbms_pg.py
# it opens this report.py
# then 
# file =open_excel(log_data.xlsx)
# open a interface ask the from date and to date ,ask the library name,ask the no of rows,  :
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
# open a interface
# page=interface
# page with heading report:
#     text username:
#         entry for username
#     text password:
#         entry for password
#     text from_date:
#         entry for from date:
#             option show the calender to make work easy
#     text to_date:
#         entry for to date:
#             option show the calender to make work easy
#     text membership category:
#         entry for membership category:
#             show the options ["UG", "PG", "Research Scholar", "Faculty", "Staff", "External Users", "Alumni", "Family","ALL"]
#     text sorting order:
#         entry for sorting order:
#             show the options ["Ascending","Descending"]
#     text library name:
#         entry for library name:
#             show the options ["Nila","Sahyadri"]
            
#     data =open the log_data.xlsx
#     data=data(from date to to date)
#     data=data[membership category]
#     data add column "count":
#             if library name=="Nila":
#                 go through all the data where library_name="Nila":
#                     count =the total number of times each person repeated:
#                     data =data[without date,checkin,checkout]
#                     data=data(each person only single time) and a new column count containing the count
#             elif library name=="Sahyadri":
#                 go through all the data where library_name="Sahyadri":
#                     count =the total number of times each person repeated:
#                     data =data[without date,checkin,checkout]
#                     data=data(each person only single time) and a new column count containing the count
#                     data=data(entry of sorting order)
#             else:
#                 go through all the data:
#                     count =the total number of times each person repeated:
#                     data =data[without date,checkin,checkout]
#                     data=data(each person only single time) and a new column count containing the count
#                     data=data(entry of sorting order)
#     add button generate Report:
#         when pressed: 
#             the final data is displayed 
#     add button save:
#         make a pdf with these data as inputs :
#             if page is finished then new page opened and continue the data
#             a= whether clicked is Ascending or Descending
#             open the present folder and name the file as user_wise_{a}_report
#     add button back :
#         destroy this interface
import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
import psycopg2
import datetime
from tkcalendar import DateEntry
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from fontsize import get_text_width

class ReportGenerator:
    def __init__(self, root):
        self.root = root
        self.previous_window = None  # To store the previous window
        self.DATA = ""
        self.membership_value = False
        self.Membership_type = ""
        self.serial_number=0
        self.earliest_date = self.get_earliest_date()
        self.create_interface()

    def get_earliest_date(self):
        file_path = "log_data.xlsx"
        data = pd.read_excel(file_path)
        data['date'] = pd.to_datetime(data['date'])
        return data['date'].min()

    def create_interface(self):
        self.frame = tk.Frame(self.root)
        self.frame.grid(sticky='nsew')
        tk.Label(self.frame, text="Report", font=("Helvetica", 24)).grid(row=0, column=1, columnspan=2, pady=10, sticky="ew")
        tk.Label(self.frame, text="       ", font=("Helvetica", 24)).grid(row=1, column=1, columnspan=2, pady=10, sticky="ew")

        # Username
        tk.Label(self.frame, text="User Name", font=("Helvetica", 14)).grid(row=2, column=0, pady=10, sticky="w")
        self.username = tk.Entry(self.frame, font=("Helvetica", 14))
        self.username.grid(row=2, column=1, pady=10, sticky="w")

        # Password
        tk.Label(self.frame, text="Password", font=("Helvetica", 14)).grid(row=2, column=2, pady=10, sticky="w")
        self.password = tk.Entry(self.frame, show="*", font=("Helvetica", 14))
        self.password.grid(row=2, column=3, pady=10, sticky="w")
        self.show_password_var = tk.IntVar()
        tk.Checkbutton(self.frame, text="Show", variable=self.show_password_var, command=self.toggle_password, font=("Helvetica", 16)).grid(row=2, column=5, columnspan=2, pady=10)

        # From date
        tk.Label(self.frame, text="From Date (DD-MM-YYYY)", font=("Helvetica", 14)).grid(row=3, column=0, pady=10, sticky="w")
        self.from_date_entry = DateEntry(self.frame, date_pattern='dd-mm-yyyy', font=("Helvetica", 14), year=self.earliest_date.year, month=self.earliest_date.month, day=self.earliest_date.day)
        self.from_date_entry.grid(row=3, column=1, pady=10, sticky="w")

        # To date
        tk.Label(self.frame, text="To Date (DD-MM-YYYY)", font=("Helvetica", 14)).grid(row=3, column=2, pady=10, sticky="w")
        self.to_date_entry = DateEntry(self.frame, date_pattern='dd-mm-yyyy', font=("Helvetica", 14))
        self.to_date_entry.grid(row=3, column=3, pady=10, sticky="w")

        # Membership category
        tk.Label(self.frame, text="Membership Category", font=("Helvetica", 14)).grid(row=4, column=0, pady=10, sticky="w")
        self.membership_var = tk.StringVar()
        self.membership_option = tk.OptionMenu(self.frame, self.membership_var, "UG", "PG", "Research Scholar", "Faculty", "Staff", "External Users", "Alumni", "Family", "ALL")
        self.membership_option.grid(row=4, column=1, pady=10, sticky="w")

        # Sorting order
        tk.Label(self.frame, text="Sorting Order", font=("Helvetica", 14)).grid(row=4, column=2, pady=10, sticky="w")
        self.sorting_var = tk.StringVar()
        self.sorting_option = tk.OptionMenu(self.frame, self.sorting_var, "Ascending", "Descending")
        self.sorting_option.grid(row=4, column=3, pady=10, sticky="w")

        # Library name
        tk.Label(self.frame, text="Library Name", font=("Helvetica", 14)).grid(row=4, column=4, pady=10, sticky="w")
        self.library_name_var = tk.StringVar()
        self.library_name_option = tk.OptionMenu(self.frame, self.library_name_var, "Nila", "Sahyadri", "Both")
        self.library_name_option.grid(row=4, column=5, pady=10, sticky="w")

        # Data display
        self.data_display = tk.Text(self.frame, font=("Helvetica", 12), height=25, width=100)
        self.data_display.grid(row=5, column=0, columnspan=4, pady=10, sticky='w')

        # Report button
        tk.Button(self.frame, text="Generate Report", command=self.generate_report, font=("Helvetica", 14)).grid(row=6, column=0, columnspan=2, pady=10)

        # Save button
        tk.Button(self.frame, text="Save", command=self.save_report, font=("Helvetica", 14)).grid(row=6, column=2, columnspan=2, pady=10)

        # Back button
        tk.Button(self.frame, text="Back", command=self.go_back, font=("Helvetica", 14)).grid(row=7, column=0, columnspan=4, pady=10)

    def toggle_password(self):
        if self.show_password_var.get():
            self.password.config(show="")
        else:
            self.password.config(show="*")
    def assign_SI_NO():
        return 0
    def generate_report(self):
        from_date = self.from_date_entry.get_date().strftime('%d-%m-%Y')
        to_date = self.to_date_entry.get_date().strftime('%d-%m-%Y')
        membership_type = self.membership_var.get()
        sorting_order = self.sorting_var.get()
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
                self.membership_value = False

                # Filter data based on date range and library name
                data['date'] = pd.to_datetime(data['date'])
                data = data[(data['date'] >= from_date) & (data['date'] <= to_date)]
                libraries = ["Nila", "Sahyadri"]
                memberships = ["UG", "PG", "Research Scholar", "Faculty", "Staff", "External Users", "Alumni", "Family"]
                if library_name in libraries:
                    data = data[data['library_name'] == library_name]
                if membership_type in memberships:
                    data = data[data['program'] == membership_type]
                    self.membership_value = True

                if data.empty:
                    messagebox.showinfo("No Data", "No data found for the given criteria.")
                    return
                data.drop(columns=['log_id','checkin','library_name','date','type', 'checkout'], inplace=True, errors='ignore')

                # Adding count
                visit_counts = data['id'].value_counts().to_dict()
                data['Count'] = data['id'].map(visit_counts)

                # Display each person's details only once
                data = data.drop_duplicates(subset='id')
                # si_no=data['id'].value_counts().to_dict()
                # data['SI.NO']=data['id'].map(si_no)

                # Sorting the data
                if sorting_order == "Ascending":
                    data.sort_values(by='Count', inplace=True, ascending=True)
                else:
                    data.sort_values(by='Count', inplace=True, ascending=False)

                self.display_data(data)
                si_no=data['id'].value_counts().to_dict()
                data['S.NO']=data['id'].map(si_no)
                self.DATA = data
                conn.close()

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def display_data(self, data):
        self.data_display.delete('1.0', tk.END)
        formatted_data = data.to_string(index=False)
        self.data_display.insert(tk.END, formatted_data)

    def save_report(self):
        if self.DATA is None:
            messagebox.showerror("Error","No report data available to save")
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        sorting_order = self.sorting_var.get().lower()
        
        file = f"user_wise_{sorting_order}_report_{current_date}.pdf"
        if self.membership_value:
            file=f"{self.Membership_type}_wise{sorting_order}_report_{current_date}.pdf"
        pdf_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save report as",
            initialfile=file
        )

        if pdf_path:
            self.create_pdf(pdf_path)


    def create_pdf(self, pdf_path):
        try:
            if self.DATA is None:
                return
            c = canvas.Canvas(pdf_path, pagesize=letter)
            width, height = letter

            c.drawString(30, height - 30, "Library Log Report")
            #define column headers and positions
            headers = ['S.NO','id','name','program','department','Count']
            col_widths=[30,80,160,100,200,30]
            y_start=height-50
            line_height=20
            line_gap=10
            #Draw headers
            x=10
            for header,width in zip(headers,col_widths):
                c.drawString(x,y_start,header)
                x+=width
            # Draw data rows
            y=y_start-20
            two_rows=False
            fontsize=10
            for _,row in self.DATA.iterrows():
                c.setFont("Helvetica", fontsize)
                #check if there is enough space for another row,add a new page if not
                if y<2*line_height+line_gap:
                    c.showPage()
                    y=height-50
                    x=10
                    #Redraw the headers on the page
                    for header,width in zip(headers,col_widths):
                        c.drawString(x,y,header)
                        x+=width
                    y-=20
                
                x=10
                for col,width in zip(headers,col_widths):
                    c.setFont("Helvetica", fontsize)
                    
                    if col=='S.NO':
                        self.serial_number+=1
                        value=str(self.serial_number)
                    else:
                        value=str(row[col])
                    font_name="Helvetica.ttf"
                    font_size=fontsize
                    # a=width(value,"Helvetica",12)
                    a=get_text_width(value,font_name,font_size)
                    print(a)
                    if a>width:
                        name_parts=value.split()
                        print("hahaha")
                        first_name=' '.join(name_parts[:-1])
                        last_name=name_parts[-1]
                        c.drawString(x,y,first_name)
                        c.drawString(x,y-10,last_name)
                        two_rows=True
                    else: 
                        c.drawString(x,y,value)
                    x+=width
                if two_rows:
                    y-=30
                    two_rows=False
                else:
                    y-=20
             
            c.showPage()
            c.save()
            
            messagebox.showinfo("Info",f"Report saved successfully as {pdf_path} ")
        except Exception as e:
            messagebox.showinfo("Error",f"Unable to save the file{e}")

        # # Split data into chunks to fit on PDF pages
        # max_rows_per_page = 50  # Adjust as needed
        # chunks = [self.DATA[i:i + max_rows_per_page] for i in range(0, len(self.DATA), max_rows_per_page)]

        # # Adding column headers
        # columns = list(self.DATA.columns)
        # header_text = ", ".join(columns)

        # for chunk_idx, chunk_data in enumerate(chunks):
        #     if chunk_idx > 0:
        #         c.showPage()  # Start a new page for each chunk after the first

        #     # Add headers
        #     c.drawString(30, height - 50, header_text)
        #     text_y = height - 70

        #     # Add data table
        #     for _, row in chunk_data.iterrows():
        #         row_text = ", ".join(str(value) for value in row)
        #         c.drawString(30, text_y, row_text)
        #         text_y -= 10


    def go_back(self):
        self.frame.destroy()
        self.root.destroy()

    def run(self):
        self.root.attributes('-fullscreen', True)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = ReportGenerator(root)
    app.run()
    root.mainloop()
