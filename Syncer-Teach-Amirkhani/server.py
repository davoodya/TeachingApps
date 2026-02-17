from math import trunc

from select import select

from settings import CLIENT_IP, CLIENT_RECEIVE_PORT
import socket
from base64 import decode
from threading import Thread
import pyperclip
from os import makedirs, path, remove
from shutil import make_archive

import tkinter as tk
from tkinter import filedialog


last_clipboard = ""


def start_receive_server(port=65432):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)

    print(f"Listening for windows clipboard on port: {port}")

    while True:
        conn, addr = server.accept()
        print(f"Connection Established from: {addr}")
        Thread(target=handle_client, args=(conn, addr)).start()

# Handle Connection from Windows Client
def handle_client(conn, addr):
    # Step 1: get first bytes to check file signal
    first_bytes = conn.recv(5)

    # Step 2: if received  a file(FILE\n)
    if first_bytes == b"FILE\n":
        # Step 2.1: Get File Name
        filename = b""
        while not filename.endswith(b"\n"):
            filename += conn.recv(1)
        filename = filename.decode("utf-8").strip()

        # Step 2.2: Get the Current directory for create "WIN_Received" directory in there:
        script_dir = path.dirname(path.abspath(__file__))
        win_received_dir = path.join(script_dir, "WIN_Received")
        makedirs(win_received_dir, exist_ok=True)
        save_path = path.join(win_received_dir, filename)

        # Step 2.3: Save File Into Disk
        with open(save_path, "wb") as f:
            while True:
                data = conn.recv(4096)
                if not data:
                   break
            f.write(data)
        print(f"[✅] File received from Windows and Saved to {save_path}")

    # Step 3: Else, receive clipboard
    else:
        # step 3.1: Receive data from Client
        data = first_bytes + conn.recv(4096)

        # Step 3.2: Decode received data
        try:
            decoded = data.decode("utf-8")
        except Exception as e:
            print(f"Error when Decoding data.\nError: {e}")
            decoded = f"Error when Decoding data.\nError: {e}"

        print(f"[✅] Received from {addr} and Data is: {decoded}")

        # Step 3.3: Write received data to a file
        with open("PC_Received.txt", "a", encoding="utf-8") as file:
            file.write(f"{decoded}\n\n")

        # Step 3.4: Copy received data into Clipboard
        pyperclip.copy(decoded)

        print(f"Received Data {decoded} Write into PC_Received.txt and Copy to Clipboard")

        # Step 3.5: Close Connection
        conn.close()

def send_clipboard_to_windows():
    """ this function sending clipboard or text to the window client """

    # Step 0: Get Last Clipboard Data
    data = pyperclip.paste()

    # Step 1: Check data is not Empty to don't send it
    if not data.strip():
        print("[⚠️] Clipboard is Empty, Nothing to send.")
        return

    # Step 2: Send Clipboard data to the Windows Client
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((CLIENT_IP, CLIENT_RECEIVE_PORT))
            s.sendall(data.encode("utf-8"))
        print("[✅] Clipboard sent to the Windows Client")

    except Exception as e:
        print(f"[🔴] Could not to Send, \nError: {e}")

# OOP Function for Select File - Used in send_files_to_windows()
def select_files():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(
        title="Select Files for Sending to Windows Client")

    return file_paths

# OOP Function for send a file to Windows Client - Used in send_files_to_windows()
def send_file_to_windows(file_path):
    try:
        # Read File
        with open(file_path, 'rb') as f:
            file_data = f.read()

        # Get File Name
        file_name = path.basename(file_path)

        # Create Socket and Connect to Windows Client
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((CLIENT_IP, CLIENT_RECEIVE_PORT))

        # Send File Signal, File Name, File Data to Windows Client
        sock.sendall(b"FILE\n")
        sock.sendall(f"{file_name}\n".encode("utf-8"))
        sock.sendall(file_data)
        sock.close()

        print(f"[✅] Sent {file_name} to Windows Client.")

    # Handle Any Error happens
    except Exception as e:
        print(f"[!] Failed to send {file_path} to windows client. \nError: {e}")

# Send File to Windows Client
def send_files_to_windows():
    # Step 1: Get all File Paths
    file_paths = select_files()

    if file_paths:
        for file_path in file_paths:
            if path.isfile(file_path):
                send_file_to_windows(file_path)


""" This Function Give Directory path from the User and Return it"""
def select_directory():
    root = tk.Tk()
    root.withdraw()
    dir_path = filedialog.askdirectory(title="Select Directory for Sending o Windows")
    return dir_path

def send_a_file_to_windows(file_path):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Step 1: Connect Linux Server to Windows Client and Send File Signal
            sock.connect((CLIENT_IP, CLIENT_RECEIVE_PORT))
            sock.sendall(b"FILE\n")

            # Step 2: Get the filename from the file path and send it to the client
            filename = path.basename(file_path)
            sock.sendall(f"{filename}\n".encode("utf-8"))

            # Step 3: Send File Data to the Windows Client
            with open(file_path, 'rb') as file:
                while True:
                    data = file.read(4096)
                    if not data:
                        break
                    sock.sendall(data)
        print(f"[✅] File {filename} Sent to Windows Client")

    except Exception as e:
        print(f"[! Could not sending {file_path} to the Windows Client. \nError: {e}")


""" this function send a directory as zip file to the Windows Client """
def send_directory_to_windows():
    # Step 1: Get directory path
    dir_path = select_directory()

    # Step 2: Check Selected Directory to be is Directory
    if dir_path and path.isdir(dir_path):
        archive_path = ''
        try:
            # Step 3: Create a ZIP Archive of selected directory
            basename = path.basename(dir_path)
            archive_path = f"/tmp/{basename}_archive.zip"
            make_archive(archive_path.replace('.zip', ''), 'zip', dir_path)
        except Exception as e:
            print(f"[!] {dir_path} Archiving not possible. \nError: {e}")

        try:
            # Step 4: Send Zip File to the Windows Client
            send_a_file_to_windows(archive_path)

            # Step 5: Remove Archive File after Sending
            remove(archive_path)
            print(f"[✅] Directory {dir_path} sent to Windows Client as ZIP File")

        except Exception as e:
            print(f"[!] Could not sending {dir_path} to Windows Client.!\n Error: {e}")

            if path.exists(archive_path):
                remove(archive_path)
    else:
        print(f"[!] {dir_path} is not a valid directory Or not selected")


def main():
    print("""
    [⌨️]Hotkeys:
    
    - CTRL + SHIFT + F1: Send Clipboard to Windows
    - CTRL + SHIFT + F2: Send a File to Windows
    - CTRL + SHIFT + F3: Send Files to Windows
    - CTRL + SHIFT + F4: Send Directory to Windows
    
    """)

    start_receive_server()
    # Thread(target=start_receive_server, daemon=True).start()


if __name__ == "__main__":
    main()
















