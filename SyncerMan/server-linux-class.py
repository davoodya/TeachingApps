import socket
import keyboard
from time import sleep
from pyperclip import copy, paste
from threading import Thread, Event
from os import path, makedirs, remove
import tkinter as tk
from tkinter import filedialog
from shutil import make_archive
from settings import WINDOWS_CLIENT_IP, CLIENT_RECEIVE_PORT

last_clipboard = ""

""" Section 3: Handle the received Data from Windows Client """
def handle_client(conn, addr):
    """ this function handling received data from the Windows client """
    first_bytes = conn.recv(5)

    # if receive a file signal from Windows
    if first_bytes == b"FILE\n":
        # Step 1: get file name
        filename = b""
        while not filename.endswith(b"\n"):
            filename += conn.recv(1)
        filename = filename.decode().strip()

        # Step 2: get the current path of the script to create "WIN_Received" directory in there
        #current_dir = os.getcwd()
        script_dir = path.dirname(path.abspath(__file__))
        windows_received_dir = path.join(script_dir, "WIN_Received")

        makedirs(windows_received_dir, exist_ok=True)
        save_path = path.join(windows_received_dir, filename)

        # Step 3: Save file into disk
        with open(save_path, "wb") as f:
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                f.write(data)
        print(f"[💾] File received from Windows and saved to {save_path}")

    # else, receive clipboard content
    else:
        # Step 0: Receive data from the Windows client
        data = first_bytes + conn.recv(4096)

        # Step 1: Decode the received data
        try:
            decoded = data.decode("utf-8")
        except Exception as e:
            decoded = f"[✗] Could not decode clipboard content. Error: {e}"

        print(f'[⇧] Received from Windows: {decoded}')

        # Step 2: Write received data to a file
        with open("PC_Received.txt", "a", encoding="utf-8") as file:
            file.write(decoded + "\n\n")

        # Step 3: Copy the received data to the clipboard
        copy(decoded)
        print("[✓] Data written to PC_Received.txt and copied to clipboard.")


    # End Step: Close Connection
    conn.close()

""" Section 2: Start Listening to the Windows Client """
def start_receive_server(port=65432):
    """ this function start listening to the Windows client on port=65432 """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)
    print(f"[📡] Listening for Windows Clipboard on port: {port}")

    while True:
        conn, addr = server.accept()
        Thread(target=handle_client, args=(conn, addr)).start()


""" Section 4: Send Clipboard to Windows Client """
def send_clipboard_to_windows(data="1"):
    global last_clipboard
    """ this function sends clipboard data from linux server to the Windows client """
    # Step 1: Get clipboard data if not argument is passed
    if data == "1":
        data = paste()

    # Step 2: Check if clipboard is empty don't send it
    if not data.strip():
        print("[!] Clipboard is empty. Nothing to send.")
        return

    # Step 3: Send clipboard data to the Windows client
    if data != last_clipboard:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((WINDOWS_CLIENT_IP, CLIENT_RECEIVE_PORT))
                s.sendall(data.encode("utf-8"))

            print(f"\n[✓] Sent clipboard({data}) to Windows.")
            last_clipboard = data

        except Exception as e:
            print(f"[✗] Could not send to Windows: {e}")
    else:
        print("[✓] Clipboard Unchanged, not sent.")

""" Section 10: Define send_text Callback function for sending input texts to windows"""
def send_text_to_windows():
    manager.release_keys('ctrl', 'shift', 'u')
    keyboard.unhook_all_hotkeys()
    try:
        data = input("enter text(sending to Windows): ")
        if data.strip():  # if a text is empty
            send_text_directly(data)
        else:
            print("[!] No text entered.")
    finally:
        manager.reset_hotkeys()

def send_text_directly(data):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((WINDOWS_CLIENT_IP, CLIENT_RECEIVE_PORT))
            s.sendall(data.encode("utf-8"))
        print(f"[✓] Sent {data} to Windows.")
    except Exception as e:
        print(f"[✗] Could not send to Windows: {e}")
        manager.reset_hotkeys()

def send_files_to_windows():
    # Step 1: get the file path => Simulate => def select_files() => return file_paths
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(title="Select Files for Sending to Windows")

    # Step 2: if file_paths is not empty, iterate over all selected files => Simulate => send_files_to_windows()
    if file_paths:
        for file_path in file_paths:
            if path.isfile(file_path):
                # Step 3: send a file to windows => Simulate => send_file_to_windows(file_path)
                try:
                    with open(file_path, 'rb') as f:
                        file_data = f.read()

                    file_name = path.basename(file_path)
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((WINDOWS_CLIENT_IP, CLIENT_RECEIVE_PORT))
                    sock.sendall(b"FILE\n")
                    sock.sendall(f"{file_name}\n".encode())
                    sock.sendall(file_data)
                    sock.close()
                    print(f"[✓] Sent {file_name} to Windows.")

                except Exception as e:
                    print(f"[!] Failed to send {file_path} to Windows:\nError: {e}")

def select_directory():
    root = tk.Tk()
    root.withdraw()
    dir_path = filedialog.askdirectory(title="Select Directory for Sending to Windows")
    return dir_path

def send_file_to_windows(file_path):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to the Linux server and send the file signal
            sock.connect((WINDOWS_CLIENT_IP, CLIENT_RECEIVE_PORT))
            sock.sendall(b"FILE\n")

            # get the filename and send it to the linux server
            filename = path.basename(file_path)
            sock.sendall(f"{filename}\n".encode())

            # send file data to the linux server
            with open(file_path, 'rb') as f:
                while True:
                    data = f.read(4096)
                    if not data:
                        break
                    sock.sendall(data)
        print(f"[✓] File {filename} sent to Windows Client.")

    except Exception as e:
        print(f"[!] Could not send file({filename}) to Windows Client.!\nError: {e}")

def send_directory_to_windows():
    # Step 1: Get the directory path
    dir_path = select_directory()
    # if dir_path entered and it is a directory
    if dir_path and path.isdir(dir_path):
        archive_path = ''
        try:
            # Step 2: Create a zip archive of the directory
            basename = path.basename(dir_path)
            archive_path = f"/tmp/{basename}_archive.zip"
            make_archive(archive_path.replace('.zip', ''), 'zip', dir_path)

            # Step 3: send the zip file to windows
            send_file_to_windows(archive_path)

            # Step 4: Remove the temporary zip file
            remove(archive_path)
            print(f"[✓] Directory {basename} sent as archive to Windows Client.")

        except Exception as e:
            print(f"[!] Could not send directory({dir_path}) to Windows Client.!\nError: {e}")
            if path.exists(archive_path):
                remove(archive_path)
    else:
        print(f"[!] {dir_path} is not a valid directory!.\n")



""" Section 8: Add Hotkeys Class """
class HotkeyManager:
    def __init__(self):
        self.exit_event = Event()
        self.hotkeys = [
            ('ctrl+shift+v', self.safe_send_clipboard),
            ('ctrl+shift+y', self.safe_send_text),
            ('ctrl+shift+f', self.safe_send_file_to_windows)
        ]
        self.registered_ids = []


    def start(self):
        """ Register Hotkeys & Start Hotkey System """
        # 1. Clear old hotkeys
        self._cleanup()

        # 2. Register new hotkeys
        for hotkey, callback in self.hotkeys:
            hotkey_id = keyboard.add_hotkey(hotkey, callback)
            self.registered_ids.append(hotkey_id)

        # 3. Start Hotkey Listener
        Thread(target=self._listener_thread, daemon=True).start()


    def _cleanup(self):
        """this private method removes old hotkeys """

        # 1. Iterate on all registered hotkeys, then remove them
        for hotkey_id in self.registered_ids:
            try:
                keyboard.remove_hotkey(hotkey_id)
            except:
                pass
        # 2. Clear the list of registered hotkeys
        self.registered_ids.clear()


    def _listener_thread(self):
        """ Main Thread for keeping the program running """
        while not self.exit_event.is_set():
            keyboard.wait()
            sleep(0.1)  # Prevent high CPU usage

    def stop(self):
        """ this function Stop the system """
        self.exit_event.set()
        self._cleanup()

    def safe_send_clipboard(self):
        self.release_keys('ctrl', 'shift', 'v')
        send_clipboard_to_windows()

    def safe_send_text(self):
        self.release_keys('ctrl', 'shift', 'u')
        keyboard.unhook_all_hotkeys()
        try:
            send_text_to_windows()
        finally:
            self.reset_hotkeys()

    def safe_send_file_to_windows(self):
        print("[🗃️] Files Sending Triggered: \n")
        self.release_keys('ctrl', 'shift', 'f')
        keyboard.unhook_all_hotkeys()
        try:
            send_files_to_windows()
        finally:
            self.reset_hotkeys()

    def reset_hotkeys(self):
        if 'manager' in globals():
            manager.stop()
            manager.start()
        else:
            print("manager not defined")

    def release_keys(self, *keys):
        for key in keys:
            try:
                keyboard.release(key)
            except:
                pass


def main():
    global manager
    print("[⌨] Hotkeys:")
    print("  - CTRL+SHIFT+V: Send Clipboard to Windows")
    print("  - CTRL+SHIFT+U: Send Text to Windows")
    print("  - CTRL+SHIFT+F: Send Files to Windows")

    """ Section 12: Start Server Receiver using Multithreading  """
    Thread(target=start_receive_server, daemon=True).start()

    manager = HotkeyManager()
    manager.start()

    try:
        while True:
            try:
                sleep(1)
                # Do nothing, just keep the program running

            except Exception as e:  # Handle any exceptions that may occur
                print(f"[!] Error: {e}")
                manager.reset_hotkeys()
                continue  # Continue to the next iteration of the loop

    except KeyboardInterrupt:
        print("\n[✗] Goodbye, Server Side shutting down...")
    finally:
        manager.reset_hotkeys()
        manager.stop()

    # while True:
    #     try:
    #         sleep(1)
    #     except KeyboardInterrupt:
    #         print("\n[✗] Exiting...")
    #         manager.reset_hotkeys()
    #         manager.stop()
    #         break



if __name__ == "__main__":
    main()