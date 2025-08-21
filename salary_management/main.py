#!/usr/bin/env python3
"""
Employee Salary Management System
Main application entry point
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow
from database.db_manager import DatabaseManager

def main():
    """Main application entry point"""
    try:
        # Initialize database
        db_manager = DatabaseManager()
        db_manager.initialize_database()
        
        # Create and run the main application
        root = tk.Tk()
        app = MainWindow(root, db_manager)
        
        # Center the window on screen
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Start the application
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("خطأ في التطبيق", f"حدث خطأ في تشغيل التطبيق:\n{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
