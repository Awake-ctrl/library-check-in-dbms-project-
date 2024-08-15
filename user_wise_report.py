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
# from library_interface import LibraryInterface

class ReportGenerator2:
    def __init__(self,root,previous_window):
        self.root = root
        self.previous_window = previous_window  # To store the previous window
        
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
        tk.Label(self.frame, text=f"""Indian Institute of Technology Palakkad
        user wise library report""",font=("Helvetica", 24)).grid(row=0, column=0, pady=10,padx=50)
        # tk.Label(self.frame, text="       ", font=("Helvetica", 24)).grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")

        # Username
        self.login_details_frame=tk.Frame(self.frame)
        self.login_details_frame.grid(row=2,column=0,columnspan=3,padx=50,sticky="ew")
        
        
        self.username_label=tk.Label(self.login_details_frame, text="User Name", font=("Helvetica", 14))
        self.username_label.grid(row=0, column=0, pady=10,padx=30)
        self.username = tk.Entry(self.login_details_frame, font=("Helvetica", 14))
        self.username.grid(row=0, column=1, pady=10,padx=30)

        # Password
        self.password_label=tk.Label(self.login_details_frame, text="Password", font=("Helvetica", 14))
        self.password_label.grid(row=0, column=2, pady=10,padx=30)
        self.password = tk.Entry(self.login_details_frame, show="*", font=("Helvetica", 14))
        self.password.grid(row=0, column=3, pady=10, padx=30)
        self.show_password_var = tk.IntVar()
        self.password_check_button=tk.Checkbutton(self.login_details_frame, text="Show", variable=self.show_password_var, command=self.toggle_password, font=("Helvetica", 16))
        self.password_check_button.grid(row=0, column=5, columnspan=2,padx=30, pady=10)

        # From date
        self.date_details_frame=tk.Frame(self.frame)
        self.date_details_frame.grid(row=3,column=0,padx=50)
        self.from_date_label=tk.Label(self.date_details_frame, text="From Date (DD-MM-YYYY)", font=("Helvetica", 14))
        self.from_date_label.grid(row=0, column=0, pady=10,padx=30,)
        self.from_date_entry = DateEntry(self.date_details_frame, date_pattern='dd-mm-yyyy', font=("Helvetica", 14), year=self.earliest_date.year, month=self.earliest_date.month, day=self.earliest_date.day)
        self.from_date_entry.grid(row=0, column=1, pady=10, padx=30)

        # To date
        self.to_date_label=tk.Label(self.date_details_frame, text="To Date (DD-MM-YYYY)", font=("Helvetica", 14))
        self.to_date_label.grid(row=0, column=2, pady=10, padx=30)
        self.to_date_entry = DateEntry(self.date_details_frame, date_pattern='dd-mm-yyyy', font=("Helvetica", 14))
        self.to_date_entry.grid(row=0, column=3, pady=10, padx=30)

        # Membership category
        self.type_details_frame=tk.Frame(self.frame)
        self.type_details_frame.grid(row=4,column=0,padx=50)
        self.membership_type_label=tk.Label(self.type_details_frame, text="Membership Category", font=("Helvetica", 14))
        self.membership_type_label.grid(row=0, column=0, pady=10, padx=30)
        self.membership_var = tk.StringVar()
        self.membership_option = tk.OptionMenu(self.type_details_frame, self.membership_var, "UG", "PG", "Research Scholar", "Faculty", "Staff", "External Users", "Alumni", "Family", "ALL")
        self.membership_option.grid(row=0, column=1, pady=10, padx=30)

        # Sorting order
        self.sort_label=tk.Label(self.type_details_frame, text="Sorting Order", font=("Helvetica", 14))
        self.sort_label.grid(row=0, column=2, pady=10,padx=30)
        self.sorting_var = tk.StringVar()
        self.sorting_option = tk.OptionMenu(self.type_details_frame, self.sorting_var, "Ascending", "Descending")
        self.sorting_option.grid(row=0, column=3, pady=10, padx=30)

        # Library name
        self.library_name_label=tk.Label(self.type_details_frame, text="Library Name", font=("Helvetica", 14))
        self.library_name_label.grid(row=0, column=4, pady=10, padx=30)
        self.library_name_var = tk.StringVar()
        self.library_name_option = tk.OptionMenu(self.type_details_frame, self.library_name_var, "Nila", "Sahyadri", "Both")
        self.library_name_option.grid(row=0, column=5, pady=10,padx=30)

        # Data display
        self.data_display_frame=tk.Frame(self.frame)
        self.data_display_frame.grid(row=5, column=0, pady=10, sticky='ew',padx=50)
        
        
        self.data_display = tk.Text(self.data_display_frame, font=("Helvetica", 12), height=25, width=100)
        self.data_display.grid(row=0, column=0, pady=10, sticky='ew',padx=30)
        
        self.footer_frame=tk.Frame(self.frame)
        self.footer_frame.grid(row=6, column=0, pady=10, sticky='ew',padx=50)
        # Report button
        tk.Button(self.footer_frame, text="Generate Report", command=self.generate_report, font=("Helvetica", 14)).grid(row=0, column=0, pady=10,padx=30)

        self.save_button=tk.Button(self.footer_frame, text="Save", command=self.show_save_options, font=("Helvetica", 14))
        self.save_button.grid(row=0, column=4,  pady=10,padx=30)
        # self.save_button.grid_forget()
        
        self.save_options_frame = tk.Frame(self.footer_frame)
        self.save_options_frame.grid(row=0, column=1,pady=9)
        self.save_options_frame.grid_remove()  # Hide the report options frame initially

        tk.Button(self.save_options_frame, text="Save as pdf", command=self.save_report, font=("Poppins", 16)).grid(row=0, column=0, padx=30)
        tk.Button(self.save_options_frame, text="Save as excel", command=self.save_as_excel, font=("Poppins", 16)).grid(row=0, column=1, padx=0)

        # Back button
        tk.Button(self.footer_frame, text="Back", command=self.go_back, font=("Helvetica", 14)).grid(row=1, column=0, pady=10,padx=30)

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
            c.drawString(x, y_start, "_" * 130)
            y_start-=11
            for header,width in zip(headers,col_widths):
                x-=1
                c.drawString(x, y_start, "|")
                x+=5
                c.drawString(x,y_start,header)
                x+=width-5
            c.drawString(x, y_start, "|")
            y_start-=9
            x=10
            c.drawString(x, y_start, "_"*130)
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
        
    
    def save_as_excel(self):
        if self.DATA is None or self.DATA.empty:
            messagebox.showinfo("info","no data to save")
            return
        save_path=filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files","*.xlsx")],
            title="Save as Excel",
            initialfile="date_wise_report.xlsx"
        )
        if save_path:
            try:
                data=self.DATA.drop(columns=['S.NO'], errors='ignore')
                
                data.to_excel(save_path,index=False)
                messagebox.showinfo("info",f"Data saved successfully as {save_path}")
            except Exception as e:
                messagebox.showerror("Error",f"Failed to save Excel file: {e}")
    def show_save_options(self):
        self.save_button.grid_forget()
        # self.save_options_frame.grid(row=6, column=1, columnspan=2, pady=10)
        self.save_options_frame.grid(row=0, column=1,pady=9)
        self.root.after(10000, self.reset_page)
        
        # print("ok")
    def reset_page(self):
        self.save_options_frame.grid_remove()
        # self.save_button.grid(row=6, column=1, columnspan=2, pady=5)
        self.save_button.grid(row=0, column=4,  pady=10)
        
       
    def go_back(self):
        self.frame.destroy()
        self.previous_window.create_library_interface()
        # self.previous_window(self.LIBRARY_NAME)

    def run(self):
        self.root.attributes('-fullscreen', True)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = ReportGenerator(root)
    app.run()
    root.mainloop()
