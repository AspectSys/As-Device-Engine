## ⚠️ Important Notes: FTDI D3XX Driver Installation

> 💡 These instructions are essential for using this hardware and Python API correctly on Windows.

### ✅ Supported Driver Version

This application is tested and supported with the following FTDI D3XX driver version:

**🔧 Required driver version: `1.3.0.10`**

Using a different version (e.g., newer ones like `1.4.x`) may lead to unexpected behavior or incompatibility with the bundled `ftd3xx.dll`.

---

## 🖥️ Driver Installation Instructions

There are currently **two ways** to install the required FTDI D3XX driver:

---

### 🔗 Option 1: Manual Download from FTDI (Recommended for Now)

1. Go to the official FTDI D3XX driver page:  
   👉 [https://ftdichip.com/drivers/d3xx-drivers/](https://ftdichip.com/drivers/d3xx-drivers/)

2. Download the driver for your system (Windows 10/11 64-bit is typical)

3. Unzip the archive, then:
   - Right-click `setup.exe`
   - Choose **“Run as administrator”**
   - Follow the installation steps

> **Important:** Make sure to install **version `1.3.0.10`** specifically (if available), as this is the version this application has been tested with.

---

### 🛠 Option 2: Use the Provided Installer (**TBD**)

_We will soon provide a pre-packaged installer with the correct driver version._

This will:
- Install the correct FTDI driver version automatically
- Ensure compatibility with this Python API
- Avoid automatic updates that may cause issues

📌 **Stay tuned** — the installer will be linked here once available.

---

### 🧪 Verifying Driver Version

You can verify the installed FTDI driver version by running this command in PowerShell:

```powershell
Get-WmiObject Win32_PnPSignedDriver | Where-Object { $_.DeviceID -like "*VID_0403*" -and $_.DeviceID -like "*PID_601*" } | Select-Object DeviceName, DriverVersion
```

Expected output should contain *FTDI FT601 USB 3.0 Bridge Device 1.3.0.10* 