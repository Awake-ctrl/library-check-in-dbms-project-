import matplotlib.pyplot as plt
from io import BytesIO

# Sample data creation (you can replace this with your actual data)
import pandas as pd
data = pd.DataFrame({
    'type': ['Student', 'Teacher', 'Staff', 'Student', 'Staff', 'Teacher', 'Student', 'Staff'],
    'program': ['Program A', 'Program B', 'Program C', 'Program A', 'Program B', 'Program C', 'Program A', 'Program B'],
    'department': ['Dept X', 'Dept Y', 'Dept Z', 'Dept X', 'Dept Y', 'Dept Z', 'Dept X', 'Dept Y']
})

# Create a figure with 3x1 layout (3 subplots stacked vertically)
fig, axes = plt.subplots(3, 1, figsize=(12, 18))  # Increase the size with figsize

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

plt.tight_layout()  # Adjust layout to minimize overlap

# Save the pie charts to a BytesIO object
pie_charts = BytesIO()
plt.savefig(pie_charts, format='png')
plt.close(fig)
pie_charts.seek(0)

# The pie_charts object now contains the image data and can be used to embed in PDFs, etc.
