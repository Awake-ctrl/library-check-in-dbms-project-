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
from reportlab.lib.pagesizes import A4,LETTER
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.utils import ImageReader
import datetime
from tkcalendar import DateEntry
from fontsize import get_text_width
from changefont import change_font_size
from header import header_name

class ReportGenerator:
    def __init__(self, root):
        self.root = root
        self.previous_window = None # To store the previous window
        self.DATA=""
        self.membership_value=False
        self.Membership_type=""
        self.first_page=True
        self.serial_number=0
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
                data.drop(columns=['log_id'], inplace=True, errors='ignore')
                self.membership_value=False
                # Filter data based on date range and library name

                data['date'] = pd.to_datetime(data['date'])
                print(data['date'])
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
                si_no=data['id'].value_counts().to_dict()
                data['S.NO']=data['id'].map(si_no)
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
        data=str(data)
        kappa=change_font_size(data)
        self.DATA=kappa
        # Insert the formatted data into the Text widget
        self.data_display.insert(tk.END, kappa)
            
   
    def create_pie_charts(self,data,membership_value,Membership_type):
        try:
            fig, axes = plt.subplots(3,1, figsize=(8.27,11.69))
            
            #font sizes
            label_font_size=12
            autopct_font_size=11
            title_font_size=18
            
            # axes[0,0].axis("off")
            
            # Pie chart for type of person
            type_counts = data['type'].value_counts()
            wedges,texts,autotexts=axes[0].pie(
                type_counts,
                labels=type_counts.index, 
                autopct='%1.1f%%',
                textprops={'fontsize':label_font_size},
                pctdistance=0.85
                )
            type_text_info=[(text.get_text(),autotext.get_text(),type_counts[index]) for index,(text,autotext) in enumerate(zip(texts,autotexts))]
            for text in texts + autotexts:
                text.set_fontsize(label_font_size)
            for autotext in autotexts:
                autotext.set_fontsize(autopct_font_size)
            
            axes[0].set_title('Type of Person',fontsize=title_font_size)
            # axes[0,2].axis("off")
            
            # Pie chart for program
            program_counts = data['program'].value_counts()
            wedges,texts,autotexts=axes[1].pie(
                program_counts,
                labels=program_counts.index,
                autopct='%1.1f%%',
                textprops={'fontsize':label_font_size},
                pctdistance=0.85
                )
            program_text_info=[(text.get_text(),autotext.get_text(),program_counts[index]) for index ,(text,autotext) in enumerate(zip(texts,autotexts))]
            for text in texts + autotexts:
                text.set_fontsize(label_font_size)
            for autotext in autotexts:
                autotext.set_fontsize(autopct_font_size)
            axes[1].set_title('Program of Person',fontsize=title_font_size)
            # axes[0,4].axis("off")
            # axes[1,1].axis("off")
            # axes[1,2].axis("off")
            # axes[2,0].axis("off")
            
            # Pie chart for department
            # axes[1,0].axis("off")
            # axes[1,1].axis("off")
            label_font_size=10
            
            department_counts = data['department'].value_counts()
            wedges,texts,autotexts=axes[2].pie(
                department_counts, 
                labels=department_counts.index, 
                autopct='%1.1f%%',
                textprops={'fontsize':label_font_size},
                pctdistance=0.85
                )
            department_text_info=[(text.get_text(),autotext.get_text(),department_counts[index]) for index ,(text,autotext) in enumerate(zip(texts,autotexts))]
            for text in texts+autotexts:
                text.set_fontsize(label_font_size)
            for autotext in autotexts:
                autotext.set_fontsize(autopct_font_size)
            axes[2].set_title('Department of Person',fontsize=title_font_size)
            # axes[1,3].axis("off")
            
            # axes[1,4].axis("off")
            #to adjust the spacing between pie_chart
            # plt.subplots_adjust(wspace=0)
            plt.subplots_adjust(hspace=1)
            plt.tight_layout()
            
            # Save the pie charts to a BytesIO object
            pie_charts = BytesIO()
            plt.savefig(pie_charts, format='png')
            plt.close(fig)
            pie_charts.seek(0)
            
            #store the information for later use
            self.text_info={
                'Type of person':type_text_info,
                'Program of person': program_text_info,
                'Department of person': department_text_info
            }
            
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
            try:
                if data is None:
                    return

                c = canvas.Canvas(pdf_path, pagesize=LETTER)
                width, height = LETTER
                
                c.drawString(30, height - 30, "Library Log Report")
                #loading the pi charts
                pie_charts_reader = ImageReader(pie_charts)
                c.drawImage(pie_charts_reader, 30, height - 750, width-60, 700)
                #define the headers and positions
                headers=['S.NO','id','name','type','program','department','date','library_name','checkin','checkout']
                col_widths=[30,55,110,40,50,150,55,45,40,40]
                y_start=height-750
                line_height=20
                line_gap=10
                x=10
                # for header,width in zip(headers,col_widths):
                #     fontsize=10
                #     header,fontsize=header_name(header,fontsize)
                #     c.setFont("Helvetica", fontsize)
                #     c.drawString(x,y_start,header)
                #     x+=width
                y=y_start-50
                # y=10
                for title, info_list in self.text_info.items():
                    if y<60:
                        c.showPage()
                        y=height-30
                    c.setFont("Helvetica-Bold", 14)
                    c.drawString(x, y, title)
                    y -= line_height
                    c.setFont("Helvetica", 12)
                    for text, pct, count in info_list:
                        c.drawString(x, y, f"{text}: {pct}, Count: {count}")
                        y -= line_height
                y-=20
                for header,width in zip(headers,col_widths):
                    if y<100:
                        c.showPage()
                        y=height-30
                    fontsize=10
                    header,fontsize=header_name(header,fontsize)
                    c.setFont("Helvetica", fontsize)
                    c.drawString(x,y,header)
                    x+=width
                y-=20
                two_rows=False
                for _,row in data.iterrows():
                    #checking enough space for another row,add a new page if not
                    
                    
                    if y<2*line_height+line_gap:
                        c.showPage()
                        y=height-50
                        x=10
                        #redraw the headers on the page
                        for header,width in zip(headers,col_widths):
                            fontsize=10
                            header,fontsize=header_name(header,fontsize)
                            c.setFont("Helvetica", fontsize)
                            c.drawString(x,y,header)
                            x+=width
                        y-=20
                    x=10
                    for col,width in zip(headers,col_widths):
                        fontsize=9
                        if col=="department":
                            fontsize=8
                        elif col =="type":
                            fontsize=8
                        elif col=="program":
                            fontsize=8
                        c.setFont("Helvetica", fontsize)
                        
    
                        if col=='S.NO':
                            self.serial_number+=1
                            value=str(self.serial_number)
                        
                        elif col=='date':
                            value=str(row[col]).split()[0]
                        elif col=="checkin":
                            value=str(row[col]).split(":")
                            value=":".join(value[:-1])
                        elif col=="checkout":
                            if str(row[col]) !="NaN":
                                value=str(row[col]).split(":")
                                value=":".join(value[:-1])
                            else:
                                value=str(row[col])
                        else:
                            value=str(row[col])
                        
                            
                        font_name="Helvetica.ttf"
                        font_size=fontsize
                        a=get_text_width(value,font_name,font_size)
                        if a>width:
                            if value=="Research Scholar":
                                c.setFont("Helvetica", 7)
                            elif value=="External Users":
                                c.setFont("Helvetica", 7)
                            else:
                                c.setFont("Helvetica", 8)
                            
                            name_parts=value.split()
                            print("hakuna matata")
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
                self.serial_number=0
                        
                if pdf_path:
                    c.showPage()
                    c.save()
                else:
                    print("kabuchi")
                messagebox.showinfo("Info",f"Report saved successfully as {pdf_path}")
            except Exception as e:
                messagebox.showinfo("Error",f"Unable to save file due to {e}")
            # # Split data into chunks to fit on PDF pages
            # max_rows_per_page = 50  # Adjust as needed
            # chunks = [data[i:i + max_rows_per_page] for i in range(0, len(data), max_rows_per_page)]
            
            # for chunk_idx, chunk_data in enumerate(chunks):
            #     if chunk_idx > 0:
            #         c.showPage()  # Start a new page for each chunk after the first
                
            #     # Add data table
            #     text_y = height - 50
            #     text_object = c.beginText(30, text_y)
            #     text_object.setFont("Helvetica", 10)
                
            #     # Convert chunk_data to string and add to PDF
            #     chunk_data_str = chunk_data.to_string(index=False)
            #     text_object.textLines(chunk_data_str)
            #     c.drawText(text_object)
                
            #     # Add pie charts
            #     if chunk_idx == 0:
            #         pie_charts_reader = ImageReader(pie_charts)
            #         c.drawImage(pie_charts_reader, 30, height - 450, width - 60, 300)
            
            # except:
            #     messagebox.showinfo("Error","unable to save")
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
    
