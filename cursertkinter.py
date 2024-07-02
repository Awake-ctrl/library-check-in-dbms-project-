import tkinter as tk
import psycopg2
from tkinter import messagebox

class LoginInterface:
    def __init__(self, root, callback):
        self.root = root
        self.callback = callback
        self.create_login_interface()

    def create_login_interface(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(expand=True, fill='both')

        tk.Label(self.login_frame, text="Login", font=("Helvetica", 24)).pack(pady=10)

        tk.Label(self.login_frame, text="Username").pack()
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack(pady=5)

        tk.Label(self.login_frame, text="Password").pack()
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.login_frame, text="Login", command=self.login, font=("Helvetica", 16)).pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = psycopg2.connect(
            dbname="your_database",
            user="your_username",
            password="your_password",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE username=%s AND password=%s', (username, password))
        result = cursor.fetchone()

        conn.close()

        if result:
            self.callback(True)
            self.root.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            self.callback(False)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginInterface(root)
    root.mainloop()
