from settings import SERVER_IP, SERVER_PORT, CLIENT_RECEIVE_PORT
import socket
from threading import Thread
import pyperclip

import tkinter as tk
from tkinter import filedialog
from os import path, environ, makedirs, remove

from shutil import make_archive

environ['TCL_LIBRARY'] = r"C:\Program Files\Python313\tcl\tcl8.6"
environ['TK_LIBRARY'] = r"C:\Program Files\Python313\tcl\tk8.6"

last_clipboard = ""


def send_clipboard(data):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT))
            s.sendall(data.encode("utf-8"))

        print(f"Data {data} Send to Linux Server.")

    except Exception as e:
        print(f"Error when Sending Data to Linux Server, Error: {e}")


""" This function Receive Clipboard from Server"""
def receive_from_linux():
    # Step 0: Create Socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Step 1: Bind Socket to the All Network Interfaces
    server.bind(("0.0.0.0", CLIENT_RECEIVE_PORT))

    # Step 2: Start Listening
    server.listen(5)

    print(f"[📥] Waiting for Clipboard Text or Files from Linux Server on Port: {CLIENT_RECEIVE_PORT}")

    # Step 3: Accept Incoming Connection
    while True:
        conn, addr = server.accept()
        print(f"[🔗] Connection Established from: {addr}")

        # Step 4: Run handle_server_connection() Function using Multi Threading
        Thread(target=handle_server_connection, args=(conn, addr)).start()


""" this function Handle Received Data(Files or Text) From Linux Server """
def handle_server_connection(conn, addr):
    first_bytes = conn.recv(5)

    # Check File Signal
    if first_bytes == b"FILE\n":
        # Get filename
        filename = b""

        while not filename.endswith(b"\n"):
            filename += conn.recv(1)
        filename = filename.decode("utf-8").strip()

        # Get the Current Directory for "Linux_Received" directory in there
        script_dir = path.dirname(path.abspath(__file__))
        linux_received_dir = path.join(script_dir, "LINUX_Received")

        makedirs(linux_received_dir, exist_ok=True)
        save_path = path.join(linux_received_dir, filename)

        # Write Received File
        with open(save_path, "wb") as f:
            data = ''
            while True:
                data = conn.recv(4096)
                if not data:
                    break
            f.write(data)

        print(f"[✅] File Received from Linux Server and Saved to: {save_path}")

    else:
        # Step 0: Receive Data from Linux Server
        data = first_bytes + conn.recv(4096)

        # Step 1: Decode Received Data
        new_data = data.decode("utf-8")

        # Step 2: Write the decoded data into a File
        with open("Server_Received.txt", "a", encoding="utf-8") as file:
            file.write(f"{new_data}\n\n")

        # Step 3: Copy decoded data into Clipboard
        pyperclip.copy(new_data)

        print(f"""
        [✅] Data Received from Linux Server.
        Data Received: {new_data}
        Receiver Info: IP: {addr[0]} | Port: {addr[1]}
        Operation: Data Write to Server_Received.txt and Copy Clipboard.
        """)

        # Step 4: Close Connection
        conn.close()

""" this function sending files from windows client to linux server """
def send_files_to_linux_server():
    # Step 1: Create TKInter and Open filedialog to select files
    root = tk.Tk()
    root.withdraw()

    file_paths = filedialog.askopenfilenames(title="Select Files for Sending to Linux Server")

    # Step 2: Send the Selected files to the Linux Server
    for file_path in file_paths:
        try:
            # Step 3: Open & Read File
            with open(file_path, 'rb') as file:
                file_data = file.read()

            # Step 4: Get the File Name from File Path
            file_name = path.basename(file_path)

            # Step 5: Create a Socket and Connect to the Linux Server
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((SERVER_IP, SERVER_PORT))

            # Step 6: Send File Signal + File Name + File Data
            sock.sendall(b"FILE\n") # Signal
            sock.sendall(f"{file_name}\n".encode()) # File Name
            sock.sendall(file_data) # File Data

            # Step 7: Close Socket & Print Help Message
            sock.close()
            print(f"[✓] Sent {file_name} to Linux Server.")

        # Step 8: Handle Exception Messages
        except Exception as e:
            print(f"[!] Failed Sending File to Linux Server.\n Error: {e}")
            print(f"- File Name: {path.basename(file_path)}")
            print(f"- File Path: {file_path}")





" this function select a directory from tkinter windows dialog "
def select_directory():
    # Step 1: Open directory selector dialog
    root = tk.Tk()
    root.withdraw()
    dir_path = filedialog.askdirectory(
        title="Select Directory for Sending to Linux Server")

    return dir_path

" this function send a file to linux server"
def send_file_to_linux(file_path):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Step 1: Connect to linux server and Send File Signal
            sock.connect((SERVER_IP, SERVER_PORT))
            sock.sendall(b"FILE\n")

            # Step 2: Get the filename and send it to linux server
            filename = path.basename(file_path)
            sock.sendall(f"{filename}\n".encode())

            # Step 3: Send file data to linux server
            with open(file_path, 'rb') as file:
                while True:
                    data = file.read(4096)
                    if not data:
                        break
                    sock.sendall(data)

        print(f"[✅] File {filename} sent to Linux Server.")

    except Exception as e:
        print(f"[!] Error when Sending a file tp linux server.\nError: {e}")


" this function send a directory as zip file to linux server"
def send_directory_to_linux():
    # Step 0: Get a directory path
    dir_path = select_directory()

    # Step 1: check dir_path entered and is directory
    if dir_path and path.isdir(dir_path):
        archive_path = ''
        try:
            # Step 2: Create a zip file from directory
            basename = path.basename(dir_path)
            archive_path = f"/tmp/{basename}_archive.zip"
            make_archive(archive_path.replace(".zip", ""),
                         "zip", dir_path)

            # Step 3: Send the zip file to linux server
            send_file_to_linux(archive_path)

            # Step 4: Remove the Temporary zip archive
            remove(archive_path)
            print(f"[✅] Directory {basename} sent to linux server as ZIP archive.\n")

        except Exception as e:
            print(f"[x] Could not send directory ({dir_path}) to Linux Server.\n Error: {e}")

            if path.exists(archive_path):
                remove(archive_path)

    else:
        print(f"[!] {dir_path} is not a valid directory!.\n")


def main():
    print("""
    [⌨️]Hotkeys:

    - CTRL + SHIFT + F1: Send Clipboard to Windows
    - CTRL + SHIFT + F2: Send a File to Windows
    - CTRL + SHIFT + F3: Send Files to Windows
    - CTRL + SHIFT + F4: Send Directory to Windows

    """)

    receive_from_linux()
    # Thread(target=start_receive_server, daemon=True).start()


if __name__ == "__main__":
    # texts = ""
    # while texts != "exit":
    #     texts = input("Enter text to send: ")
    #     send_clipboard(texts)
    #send_files_to_linux_server()
    main()


""" Continue from Testing and Send Text File(Data)"""