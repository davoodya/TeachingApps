# SyncerMan

SyncerMan is a powerful, cross-platform synchronization tool designed to bridge the gap between Windows and Linux environments. It enables real-time, bi-directional sharing of clipboard content, text messages, files, and directories over a local network using TCP sockets.

Built with Python, SyncerMan runs efficiently in the background, listening for global hotkeys to trigger instant data transfer without interrupting your workflow.

Im using this app for teaching my students. main repository of [Syncer Man](https://github.com/davoodya/Syncer) is here: https://github.com/davoodya/Syncer
Also main version of Syncer Man in the /SyncerMan-Official Directory 

## Key Features

*   **Clipboard Synchronization**: Instantly copy text on one machine and paste it on the other.
*   **Direct Text Messaging**: Send quick text inputs directly between machines.
*   **File Transfer**: Select and send multiple files securely.
*   **Directory Transfer**: Automatically archive (zip) and transfer entire folders.
*   **Global Hotkeys**: Control all actions using customizable keyboard shortcuts.
*   **Background Operation**: Runs unobtrusively with a system tray-like behavior (CLI based).

## Technical Overview

The application consists of two main scripts:
1.  **Server (Linux Side)**: Listens for incoming connections from Windows and initiates outgoing transfers.
2.  **Client (Windows Side)**: Connects to the Linux server and listens for incoming data.

Both sides utilize multi-threading to handle sending and receiving data simultaneously without blocking the user interface or hotkey listeners.

### Requirements

*   Python 3.x
*   **Dependencies**:
    *   `keyboard`: For global hotkey detection.
    *   `pyperclip`: For accessing system clipboard.
    *   `tkinter`: For file and directory selection dialogs (usually included with Python).

### Configuration

Ensure both machines are on the same local network. You may need to configure the IP addresses and ports in a `settings.py` file (not included in this overview, but required by the scripts):
*   `SERVER_IP`: IP address of the Linux machine.
*   `WINDOWS_CLIENT_IP`: IP address of the Windows machine.
*   `SERVER_PORT` & `CLIENT_RECEIVE_PORT`: Ports used for communication.

### Requirements

#### Windows (Client)
- Python 3.x
- Modules:
  - `pyperclip`
  - `keyboard`
#### Linux (Server)
- Python 3.x
- Modules:
  - `pyperclip`
  - `keyboard`
- Note: **Linux side** Must **run with `sudo`** due to `keyboard` requiring root access permission.

## Setup and Run Syncer Man 

### 0. Install Requirements 
#### 0.1: Windows 
- Install `Python 3.12` on both Windows and Linux.
- Then, on **Windows**, open PowerShell as Administrator and run:

```powershell
python -m pip install pyperclip
python -m pip install keyboard
```

#### 0.2: Linux
- Install the following libraries:

```sh
sudo pip install pyperclip
sudo pip install keyboard
```

- **Note:** The `keyboard` package must be installed with root access (`sudo`).

### 1. Update IP addresses
0. In `server-linux.py` (Linux), set the correct IP address of your Windows PC:
```python
WINDOWS_CLIENT_IP = "192.168.x.x"
```
- **Note:** Use `ipconfig` on Windows to find your correct IP address.

1. In `client-windows.py` (Windows), set the correct IP address of your Linux PC:
```python
SERVER_IP = "192.168.x.x"
```
- **Note:** Use `ifconfig` (or `ip a`) on Linux to find your correct IP address.

### 2. Define Firewall Rules for TCP/65433

#### 2.1: Windows 

##### 2.1: Using GUI
To ensure your Linux server can send data to your Windows clipboard sync client, you need to allow incoming connections on a specific TCP port (e.g., `65433`) in Windows Firewall.

0. `WIN+R => wf.msc => Inbound Rules => New Rule`
	1. Define an Allow rule for TCP port `65433`.

- OR you can use PowerShell.

##### 2.2: Using Powershell:
0. **Open PowerShell as Administrator**
   - Press `Win + S`, search for `PowerShell`
   - Right-click and choose **Run as Administrator**

1. **Run the following command**:

```powershell
New-NetFirewallRule -DisplayName "Allow Clipboard Sync" `
                    -Direction Inbound `
                    -LocalPort 65433 `
                    -Protocol TCP `
                    -Action Allow
```

2. **Verify the rule**
	- Open **Windows Defender Firewall with Advanced Security**
	- Go to **Inbound Rules**
	- Look for the rule named **"Allow Clipboard Sync"**

- ### 🛠 Notes
	- You can change `65433` to any other port number if needed — just make sure it matches your Python script.
	- Make sure your Windows machine is using a **Private or Trusted network** profile.
	- No restart is needed; the rule applies immediately.
	- This rule only opens **TCP** traffic on port `65433`.
	
##### 2.3: Note: To Delete the Rule Later (Optional)
If you want to remove this rule, run:

```powershell
Remove-NetFirewallRule -DisplayName "Allow Clipboard Sync"
```

#### 2.4: Linux Debian Based 
- If your Linux system is not using a firewall, you can skip this step.  
- If a firewall is enabled, configure it according to your Linux distribution.

##### 2.4.0: Debian Based 
0. If you are using the `ufw` firewall, add the following command:

```sh
sudo ufw allow 65433/tcp comment 'Allow Clipboard Sync'
```

1. If you want to remove the rule after uninstalling the app, use the following command:

```sh
sudo ufw delete allow 65433/tcp
```

##### 2.4.1: RedHat Based 
0. Add the rule using `firewall-cmd`:

```sh
sudo firewall-cmd --permanent --add-port=65433/tcp
sudo firewall-cmd --reload
```

1. If you want to remove the rule after uninstalling the app, use the following command:

```sh
sudo firewall-cmd --permanent --remove-port=65433/tcp
sudo firewall-cmd --reload
```

- By completing this step, your Windows and Linux systems will be ready to **receive/send data** over the network.

### 3. Run Script
0. On Linux, run the server side:

```sh
sudo python3 linux-server.py
```

0. Then, on Windows, open PowerShell as Administrator and run the client:

```powershell
python windows-client.py
```

- Note: You can change the server and client execution locations. For example, you can run the server on Windows and the client on Linux. The choice is yours.


### Keyboard Shortcuts - Should be Changed 

#### Windows Client (Sending to Linux)
| Hotkey | Action | Description |
| :--- | :--- | :--- |
| **Ctrl + Alt + C** | Send Clipboard | Sends current clipboard content to Linux. |
| **Ctrl + Alt + Y** | Send Text | Opens a prompt to type text to send to Linux. |
| **Ctrl + Alt + F** | Send Files | Opens a file dialog to select and send files. |
| **Ctrl + Alt + D** | Send Directory | Opens a dialog to select a folder, zips it, and sends it. |

#### Linux Server (Sending to Windows)
| Hotkey | Action | Description |
| :--- | :--- | :--- |
| **Ctrl + Shift + V** | Send Clipboard | Sends current clipboard content to Windows. |
| **Ctrl + Shift + U** | Send Text | Opens a prompt to type text to send to Windows. |
| **Ctrl + Shift + F** | Send Files | Opens a file dialog to select and send files. |
| **Ctrl + Shift + D** | Send Directory | Opens a dialog to select a folder, zips it, and sends it. |

### 3. Receiving Data
*   **Text/Clipboard**: Received text is automatically saved to a log file (`Linux_Received.txt` or `PC_Received.txt`) and copied to your system clipboard, ready to paste.
*   **Files**: Received files are saved automatically into a specific folder:
    *   **On Windows**: `Linux_Received/`
    *   **On Linux**: `WIN_Received/`

## Troubleshooting
*   **Connection Errors**: Ensure firewall rules allow traffic on the configured ports.
*   **Permission Errors**: On Linux, the `keyboard` library often requires root privileges (`sudo`).

- **Enjoy Script** 😊 