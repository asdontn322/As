import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import os

def run_automation():
    try:
        log_box.delete(1.0, tk.END)
        log_box.insert(tk.END, "⚙ Running automation...\n")
        result = subprocess.run(["python", "main.py"], capture_output=True, text=True)
        log_box.insert(tk.END, result.stdout)
        if result.returncode == 0:
            messagebox.showinfo("Success", "✅ Automation completed!")
        else:
            messagebox.showerror("Error", "❌ Automation failed.")
            log_box.insert(tk.END, result.stderr)
    except Exception as e:
        messagebox.showerror("Exception", str(e))

def view_logs():
    if os.path.exists("logs/automation.log"):
        with open("logs/automation.log", "r") as f:
            logs = f.read()
        log_box.delete(1.0, tk.END)
        log_box.insert(tk.END, logs)
    else:
        log_box.insert(tk.END, "No log file found.")

# GUI window
root = tk.Tk()
root.title("📊 Legacy Automation App")
root.geometry("600x400")

tk.Label(root, text="Legacy Automation GUI", font=("Helvetica", 16, "bold")).pack(pady=10)

tk.Button(root, text="▶ Run Automation", command=run_automation, width=25, bg="green", fg="white").pack(pady=5)
tk.Button(root, text="📄 View Logs", command=view_logs, width=25).pack(pady=5)

log_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15)
log_box.pack(pady=10)

root.mainloop()
