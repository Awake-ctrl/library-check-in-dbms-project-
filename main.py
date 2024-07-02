import tkinter as tk
from login import LoginInterface

if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-fullscreen', True)  # Make the window fullscreen
    app = LoginInterface(root)
    root.mainloop()
