import os
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import threading
import pyperclip
import time
import psutil  # System resource monitoring
import joblib
import logging
from datetime import datetime
from pynput import keyboard
from cryptography.fernet import Fernet  # AES-like encryption
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load trained ML model & vectorizer
clf = joblib.load("ml_ids_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Logging setup
log_file = "C:\\Users\\Public\\threat_logs.txt"
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s")

keystroke_buffer = []
last_clipboard_content = ""

# System resource tracking
cpu_usage = []
ram_usage = []

def detect_threat(input_text, source):
    """Uses ML model to classify input as benign or malicious."""
    transformed_input = vectorizer.transform([input_text])
    prediction = clf.predict(transformed_input)[0]  # Get predicted label

    if prediction != "benign":
        log_entry = f"🚨 THREAT DETECTED ({source}): {prediction} - {input_text}\n"
        logging.info(log_entry)
        update_gui(log_entry)  # Update GUI
        return True
    return False

def on_key_press(key):
    """Captures keystrokes and detects malicious input."""
    try:
        key_str = key.char if hasattr(key, 'char') and key.char else str(key)
        keystroke_buffer.append(key_str)

        # Analyze every 10 keystrokes
        if len(keystroke_buffer) >= 10:
            detect_threat(" ".join(keystroke_buffer), "Keystroke")
            keystroke_buffer.clear()  # Reset buffer
    except Exception as e:
        print(f"Error logging keystroke: {e}")

def monitor_clipboard():
    """Monitors clipboard for suspicious pasted content."""
    global last_clipboard_content
    while True:
        time.sleep(1)  # Check clipboard every second
        clipboard_content = pyperclip.paste()
        if clipboard_content != last_clipboard_content:  # Detect clipboard changes
            last_clipboard_content = clipboard_content
            detect_threat(clipboard_content, "Clipboard")

def monitor_usb_keyboards():
    """Starts monitoring all USB keyboard keystrokes."""
    print("✅ Monitoring all USB keyboards & clipboard for malicious commands...")
    with keyboard.Listener(on_press=on_key_press) as listener:
        listener.join()

def update_gui(log_entry):
    """Updates the GUI log display with new alerts."""
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, log_entry)
    log_text.config(state=tk.DISABLED)
    log_text.yview(tk.END)  # Auto-scroll to latest log

def load_logs():
    """Loads existing log entries into the GUI."""
    with open(log_file, "r") as f:
        logs = f.readlines()
    log_text.config(state=tk.NORMAL)
    log_text.delete(1.0, tk.END)
    log_text.insert(tk.END, "".join(logs))
    log_text.config(state=tk.DISABLED)

def update_system_monitor():
    """Updates system resource usage graphs in real-time."""
    global cpu_usage, ram_usage

    # Update data
    cpu_usage.append(psutil.cpu_percent())
    ram_usage.append(psutil.virtual_memory().percent)

    # Keep only the last 20 values for smooth plotting
    if len(cpu_usage) > 20:
        cpu_usage.pop(0)
        ram_usage.pop(0)

    # Update CPU graph
    ax1.clear()
    ax1.plot(cpu_usage, label="CPU Usage (%)", color="blue")
    ax1.set_ylim(0, 100)
    ax1.set_title("CPU Usage Over Time")
    ax1.legend()

    # Update RAM graph
    ax2.clear()
    ax2.plot(ram_usage, label="RAM Usage (%)", color="red")
    ax2.set_ylim(0, 100)
    ax2.set_title("RAM Usage Over Time")
    ax2.legend()

    canvas.draw()
    root.after(1000, update_system_monitor)  # Refresh every second

# 🔹 ENCRYPTION FUNCTIONS
def generate_key():
    """Generates an encryption key and saves it."""
    key = Fernet.generate_key()
    with open("encryption_key.key", "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    """Loads the encryption key from file."""
    return open("encryption_key.key", "rb").read()

def encrypt_file(file_path, key):
    """Encrypts a file using AES encryption."""
    cipher = Fernet(key)
    with open(file_path, "rb") as file:
        file_data = file.read()
    encrypted_data = cipher.encrypt(file_data)
    with open(file_path, "wb") as file:
        file.write(encrypted_data)

def encrypt_directory():
    """Encrypts all files in a selected directory."""
    dir_path = filedialog.askdirectory(title="Select Directory to Encrypt")
    if not dir_path:
        return

    key = generate_key()  # Generate a new key for encryption
    for root_dir, _, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root_dir, file)
            encrypt_file(file_path, key)

    messagebox.showinfo("Encryption Complete", f"Encrypted all files in: {dir_path}\nKey saved as encryption_key.key")

# 🔹 GUI Setup
root = tk.Tk()
root.title("USB IDS Threat Monitor & Encryption")
root.geometry("800x650")

# Logging Section
log_text = scrolledtext.ScrolledText(root, state=tk.DISABLED, wrap=tk.WORD, height=10)
log_text.pack(expand=True, fill="both")

refresh_button = tk.Button(root, text="🔄 Refresh Logs", command=load_logs)
refresh_button.pack()

# Encryption Button
encrypt_button = tk.Button(root, text="🔒 Encrypt Directory", command=encrypt_directory, bg="black", fg="white")
encrypt_button.pack(pady=10)

# System Monitoring Section
fig = Figure(figsize=(6, 3), dpi=100)
ax1 = fig.add_subplot(121)  # CPU usage graph
ax2 = fig.add_subplot(122)  # RAM usage graph

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(expand=True, fill="both")

# Start monitoring in background threads
threading.Thread(target=monitor_clipboard, daemon=True).start()
threading.Thread(target=monitor_usb_keyboards, daemon=True).start()
root.after(1000, update_system_monitor)  # Start system monitoring

load_logs()
root.mainloop()
