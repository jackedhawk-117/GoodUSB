import tkinter as tk
from tkinter import scrolledtext

def update_log():
    """Updates GUI with latest log entries."""
    with open("C:\\Users\\Public\\threat_logs.txt", "r") as f:
        logs = f.readlines()
    log_text.config(state=tk.NORMAL)
    log_text.delete(1.0, tk.END)
    log_text.insert(tk.END, "".join(logs))
    log_text.config(state=tk.DISABLED)
    root.after(3000, update_log)  # Refresh every 3 sec

# Create GUI
root = tk.Tk()
root.title("USB IDS Threat Monitor")
root.geometry("600x400")

log_text = scrolledtext.ScrolledText(root, state=tk.DISABLED, wrap=tk.WORD)
log_text.pack(expand=True, fill="both")

update_log()
root.mainloop()
