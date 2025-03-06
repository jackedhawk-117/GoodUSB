# Load Required Assemblies
Add-Type -AssemblyName System.Windows.Forms
Add-Type -TypeDefinition @"
using System;
using System.Drawing;
using System.Windows.Forms;
using System.IO;

public class IDSForm : Form {
    private Label statusLabel;
    private Button encryptButton;

    public IDSForm() {
        this.Text = "Intrusion Detection System";
        this.Size = new Size(400, 250);
        this.StartPosition = FormStartPosition.CenterScreen;

        statusLabel = new Label() { Text = "Monitoring System...", AutoSize = true, Location = new Point(20, 20) };
        encryptButton = new Button() { Text = "Encrypt Files", Location = new Point(20, 60), Enabled = false };

        encryptButton.Click += (sender, e) => {
            EncryptFiles();
        };

        this.Controls.Add(statusLabel);
        this.Controls.Add(encryptButton);

        // Monitor System Logs and Enable Encryption If Suspicious Activity is Detected
        System.Windows.Forms.Timer timer = new System.Windows.Forms.Timer();
        timer.Interval = 5000; // Check every 5 seconds
        timer.Tick += (sender, e) => {
            if (CheckForAnomalies()) {
                encryptButton.Enabled = true;
                statusLabel.Text = "Threat Detected! Encryption Available";
                statusLabel.ForeColor = Color.Red;
            } else {
                encryptButton.Enabled = false;
                statusLabel.Text = "Monitoring System...";
                statusLabel.ForeColor = Color.Black;
            }
        };
        timer.Start();
    }

    private bool CheckForAnomalies() {
        // Read last line of system_logs.csv and check if anomaly label is "1"
        try {
            string[] lines = File.ReadAllLines(@"C:\Users\Public\system_logs.csv");
            if (lines.Length > 1) {
                string lastLine = lines[lines.Length - 1];
                string[] data = lastLine.Split(',');
                return data[data.Length - 1].Trim() == "1";
            }
        } catch (Exception) { }
        return false;
    }

    private void EncryptFiles() {
        MessageBox.Show("Encryption Activated!", "Security Alert", MessageBoxButtons.OK, MessageBoxIcon.Warning);
        // Encrypt selected files (Placeholder for actual encryption logic)
    }
}
"@ -ReferencedAssemblies System.Drawing,System.Windows.Forms,System.IO

# Start GUI in Separate Thread
$thread = [System.Threading.Thread]::new({ 
    [System.Windows.Forms.Application]::Run([IDSForm]::new()) 
})
$thread.SetApartmentState("STA")
$thread.Start()

# Define CSV File Location for Logs
$logFile = "C:\Users\Public\system_logs.csv"

# Create CSV Header if File Doesn't Exist
if (-Not (Test-Path $logFile)) {
    "CPU_Usage,Network_Activity,Suspicious_Process,USB_Inserted,Anomaly_Label" | Out-File -Encoding utf8 -FilePath $logFile
}

# Function to Check for Suspicious Processes
function Check-SuspiciousProcess {
    $suspiciousProcesses = @("powershell", "cmd", "taskmgr", "regedit", "netstat", "wireshark")
    $runningProcesses = Get-Process | Select-Object -ExpandProperty ProcessName
    $found = $runningProcesses | Where-Object { $_ -in $suspiciousProcesses }
    return [int]($found.Count -gt 0) # Returns 1 if found, 0 otherwise
}

# Function to Check for USB Insertions
function Check-USBInserted {
    $usbDevices = Get-PnpDevice | Where-Object { $_.Class -eq "USB" -and $_.Status -eq "OK" }
    return [int]($usbDevices.Count -gt 0) # Returns 1 if USB is detected, 0 otherwise
}

# Function to Get Network Activity (Bytes Sent & Received)
function Get-NetworkActivity {
    $adapters = Get-NetAdapterStatistics
    return ($adapters | Measure-Object -Property BytesSentPerSec -Sum).Sum +
           ($adapters | Measure-Object -Property BytesReceivedPerSec -Sum).Sum
}

# Continuous Log Monitoring and Collection
while ($true) {
    # Collect System Data
    $cpuUsage = [math]::Round((Get-Counter '\Processor(_Total)\% Processor Time').CounterSamples.CookedValue, 2)
    $networkActivity = Get-NetworkActivity
    $suspiciousProcess = Check-SuspiciousProcess
    $usbInserted = Check-USBInserted
    $anomalyLabel = 0  # Placeholder (ML Model should predict this)

    # Format Data for CSV
    $logEntry = "$cpuUsage,$networkActivity,$suspiciousProcess,$usbInserted,$anomalyLabel"

    # Append Log Entry to File
    Add-Content -Path $logFile -Value $logEntry

    Write-Host "Log entry added: $logEntry"

    Start-Sleep -Seconds 5
}
