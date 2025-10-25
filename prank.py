import tkinter as tk
from tkinter import messagebox

def show_fake_error():
    """Displays a fake error message pop-up on the desktop."""
    root = tk.Tk()
    root.withdraw()  # Hides the main window
    messagebox.showerror("System Failure", "Error: User is having too much fun. Please stop immediately!")
    root.destroy()