import tkinter as tk

def on_button_click():
    print("Button clicked!")

root = tk.Tk()

# Frame
frame = tk.Frame(root, bg="lightgrey")
frame.pack(padx=20, pady=20)

# Label
label = tk.Label(frame, text="Enter your name:", bg="lightgrey", fg="darkblue")
label.pack(padx=10, pady=5)

# Entry
entry = tk.Entry(frame, bg="blue", fg="black")
entry.pack(padx=10, pady=5)

# Button
button = tk.Button(frame, text="Submit", bg="lightgreen", fg="black",
                   activebackground="darkgreen", activeforeground="white",
                   command=on_button_click)
button.pack(padx=10, pady=10)

root.mainloop()
