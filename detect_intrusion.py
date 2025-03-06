import os
import time
import joblib
import logging
import pyperclip
from datetime import datetime
from pynput import keyboard

# Load trained ML model & vectorizer
clf = joblib.load("ml_ids_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Logging setup
log_file = "C:\\Users\\Public\\threat_logs.txt"
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s")

keystroke_buffer = []
last_clipboard_content = ""

def detect_threat(input_text, source):
    """Uses ML model to classify input as benign or malicious."""
    transformed_input = vectorizer.transform([input_text])
    prediction = clf.predict(transformed_input)[0]  # Get predicted label

    if prediction != "benign":
        logging.info(f"🚨 THREAT DETECTED ({source}): {prediction} - {input_text}")
        print(f"⚠️ ALERT ({source}): {prediction} detected! - {input_text}")
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
        monitor_clipboard()  # Run clipboard monitoring alongside keystroke monitoring
        listener.join()

monitor_usb_keyboards()
