from matplotlib import pyplot as plt

plt.style.use("fivethirtyeight")

slices = [100, 50, 47, 36, 35, 68, 98, 9]
labels = ['UG', 'PG', 'Research Scholar', 'Faculty', 'Staff', 'External Users', 'Alumnus', 'Family']

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']

plt.pie(slices, labels=labels, colors=colors, shadow=True,
        startangle=90, autopct='%1.1f%%',
        wedgeprops={'edgecolor': 'black'})

plt.title("Category Wise Report")
plt.tight_layout()
plt.show()