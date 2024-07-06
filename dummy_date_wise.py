import tkinter as tk
from tkinter import filedialog, messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
import matplotlib.pyplot as plt
import pandas as pd
import datetime

class ReportGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Log Report Generator")
        self.text_info = {}

    def run(self):
        # Example data
        data = pd.DataFrame({
            'type': ['Student', 'Faculty', 'Student', 'Student', 'Faculty', 'Staff', 'Staff'],
            'program': ['Undergrad', 'PhD', 'Undergrad', 'Masters', 'PhD', 'Staff', 'Staff'],
            'department': ['CS', 'CS', 'EE', 'CS', 'EE', 'Admin', 'Admin']
        })
        self.create_pie_charts(data, False, None)

    def create_pie_charts(self, data, membership_value, Membership_type):
        try:
            fig, axes = plt.subplots(1, 3, figsize=(18, 6))  # Adjust the figsize as needed

            # Font sizes
            label_font_size = 14
            autopct_font_size = 12
            title_font_size = 16

            # Pie chart for type of person
            type_counts = data['type'].value_counts()
            wedges, texts, autotexts = axes[0].pie(
                type_counts,
                labels=type_counts.index,
                autopct='%1.1f%%',
                textprops={'fontsize': label_font_size},
                pctdistance=0.85
            )
            type_text_info = [(text.get_text(), autotext.get_text(), type_counts[index]) for index, (text, autotext) in enumerate(zip(texts, autotexts))]
            for text in texts + autotexts:
                text.set_fontsize(label_font_size)
            for autotext in autotexts:
                autotext.set_fontsize(autopct_font_size)
            axes[0].set_title('Type of Person', fontsize=title_font_size)

            # Pie chart for program
            program_counts = data['program'].value_counts()
            wedges, texts, autotexts = axes[1].pie(
                program_counts,
                labels=program_counts.index,
                autopct='%1.1f%%',
                textprops={'fontsize': label_font_size},
                pctdistance=0.85
            )
            program_text_info = [(text.get_text(), autotext.get_text(), program_counts[index]) for index, (text, autotext) in enumerate(zip(texts, autotexts))]
            for text in texts + autotexts:
                text.set_fontsize(label_font_size)
            for autotext in autotexts:
                autotext.set_fontsize(autopct_font_size)
            axes[1].set_title('Program of Person', fontsize=title_font_size)

            # Pie chart for department
            department_counts = data['department'].value_counts()
            wedges, texts, autotexts = axes[2].pie(
                department_counts,
                labels=department_counts.index,
                autopct='%1.1f%%',
                textprops={'fontsize': label_font_size},
                pctdistance=0.85
            )
            department_text_info = [(text.get_text(), autotext.get_text(), department_counts[index]) for index, (text, autotext) in enumerate(zip(texts, autotexts))]
            for text in texts + autotexts:
                text.set_fontsize(label_font_size)
            for autotext in autotexts:
                autotext.set_fontsize(autopct_font_size)
            axes[2].set_title('Department of Person', fontsize=title_font_size)

            plt.tight_layout()

            # Save the pie charts to a BytesIO object
            pie_charts = BytesIO()
            plt.savefig(pie_charts, format='png')
            plt.close(fig)
            pie_charts.seek(0)

            # Store text information for later use
            self.text_info = {
                'Type of Person': type_text_info,
                'Program of Person': program_text_info,
                'Department of Person': department_text_info
            }

            # Display and save PDF report
            self.display_and_save_pdf(data, pie_charts, membership_value, Membership_type)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def display_and_save_pdf(self, data, pie_charts, membership_value, Membership_type):
        # Ask the user where to save the PDF file
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        file = f"date_wise_report_{current_date}.pdf"
        if membership_value:
            file = f"{Membership_type}_wise_report_{current_date}.pdf"
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

                c = canvas.Canvas(pdf_path, pagesize=A4)
                width, height = A4

                c.drawString(30, height - 30, "Library Log Report")

                # Draw pie charts on the left side
                pie_charts_reader = ImageReader(pie_charts)
                chart_height = height / 3 - 40
                c.drawImage(pie_charts_reader, 30, height - chart_height - 30, width / 2 - 40, chart_height * 3)

                # Draw text information on the right side
                text_x = width / 2 + 10
                text_y = height - 60
                line_height = 20

                for title, info_list in self.text_info.items():
                    c.setFont("Helvetica-Bold", 14)
                    c.drawString(text_x, text_y, title)
                    text_y -= line_height
                    c.setFont("Helvetica", 12)
                    for text, pct, count in info_list:
                        c.drawString(text_x, text_y, f"{text}: {pct}, Count: {count}")
                        text_y -= line_height
                        if text_y < 60:
                            c.showPage()
                            text_y = height - 60

                c.showPage()
                c.save()
                messagebox.showinfo("Info", f"Report saved successfully as {pdf_path}")
            except Exception as e:
                messagebox.showinfo("Error", f"Unable to save file due to {e}")

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    app = ReportGenerator(root)
    app.run()
