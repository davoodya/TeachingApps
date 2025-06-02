import socket
from threading import Thread, Event
from time import sleep
import keyboard
from pyperclip import copy, paste
import tkinter as tk
from tkinter import filedialog # used for asking files for sending to linux server
from os import path, makedirs
from settings import SERVER_IP, SERVER_PORT, CLIENT_RECEIVE_PORT

last_clipboard = ""

""" Section 1: Send Clipboard to Linux Server """
def send_clipboard(text="1"):
    global last_clipboard
    # Step 1: Get clipboard data if not argument is passed
    if text == "1":
        text = paste()

    if text != last_clipboard:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((SERVER_IP, SERVER_PORT))
                sock.sendall(text.encode("utf-8"))

            if text == paste():
                print("[✓] Sent clipboard to Linux.")
                last_clipboard = text
            else:
                print(f"[✓] Sent {text} to Linux.")

        except Exception as e:
            print(f"[✗] Error sending clipboard to Linux: {e}")
    else:
        print("[✓] Clipboard Unchanged, not sent.")

""" Section 7: Define send_text Callback function for sending input texts to linux"""
def send_text_to_linux():
    manager.release_keys('ctrl', 'alt', 'y')
    keyboard.unhook_all_hotkeys()
    try:
        text = input("enter text(sending to Linux): ")
        if text.strip():  # if a text is empty
            send_text_directly(text)
        else:
            print("[!] No text entered.")
    finally:
        manager.reset_hotkeys()

def send_text_directly(text):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((SERVER_IP, SERVER_PORT))
            sock.sendall(text.encode("utf-8"))
        print(f"[✓] Sent({text}) to Linux.")

    except Exception as e:
        print(f"[✗] Could not send({text}) to Linux: {e}")
        manager.reset_hotkeys()

""" Section 5: Receive Clipboard from Linux Server """
def receive_from_linux():
    # Step 1: Create a socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Step 2: Bind the socket to the all interfaces on port 65433 and Start Listening
    server.bind(("0.0.0.0", CLIENT_RECEIVE_PORT))
    server.listen(5)

    print(f"[📥] Waiting for clipboard or files from Linux on Port: {CLIENT_RECEIVE_PORT}")

    # Step 3: Accept incoming connections
    while True:
        conn, addr = server.accept()
        #print(f"[🔗] Connection established from {addr}")
        Thread(target=handle_client_connection, args=(conn, addr)).start()

""" Section 6: Handle Received Data from Linux Server """
def handle_client_connection(conn, addr):
    first_bytes = conn.recv(5)
    # If Received data is a file
    if first_bytes == b"FILE\n":
        filename = b""
        while not filename.endswith(b"\n"):
            filename += conn.recv(1)
        filename = filename.decode().strip()

        # get the current directory for create "Linux_Received" directory in there
        #current_dir = os.getcwd()
        script_dir = path.dirname(path.abspath(__file__))
        linux_received_dir = path.join(script_dir, "Linux_Received")

        makedirs(linux_received_dir, exist_ok=True)
        save_path = path.join(linux_received_dir, filename)

        with open(save_path, "wb") as f:
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                f.write(data)

        print(f"[💾] File received from Linux and saved to {save_path}")

    # Else Received data is a text(clipboard)
    else:
        # Step 0: Receive data from the Linux server
        data = first_bytes + conn.recv(4096)

        # Step 1: Decode the received data
        decoded = data.decode("utf-8")

        # Step 2: Write received data to a file
        with open("Linux_Received.txt", "a", encoding="utf-8") as file:
            file.write(decoded + "\n\n")

        # Step 3: Copy the received data to the clipboard
        copy(decoded)

        print(f"[✓] Data Written to Linux_Received.txt and copied to clipboard.")
        print(f':: Received Data: {decoded}')

    # Step 4: Close Connection
    conn.close()

def send_files_to_linux():
    # Step 1: Open a file dialog to select files
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(title="Select Files for Sending to Linux")

    # Step 2: Send the selected files to the Linux server
    for file_path in file_paths:
        try:
            # Step 2.1: Open and read the file
            with open(file_path, 'rb') as file:
                file_data = file.read()

            # Step 2.2: Get file name
            file_name = path.basename(file_path)

            # Step 2.3: Create a socket and Connect to the Linux server
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((SERVER_IP, SERVER_PORT))

            # Step 2.4: Send the file signal + file name and file data
            sock.sendall(b"FILE\n")
            sock.sendall(f"{file_name}\n".encode())
            sock.sendall(file_data)
            # Step 2.5: Close the socket
            sock.close()
            print(f"[✓] Sent {file_name} to Linux.")

        except Exception as e:
            print(f"[!] Failed to send {file_path}: {e}")



# keyboard.add_hotkey('ctrl+alt+c', send_clipboard)
# keyboard.add_hotkey('ctrl+alt+y', lambda: send_text(send_clipboard))

""" Section 8: Add Hotkeys Class """
class HotkeyManager:
    def __init__(self):
        self.exit_event = Event()
        self.hotkeys = [
            ('ctrl+alt+c', self.safe_send_clipboard),
            ('ctrl+alt+y', self.safe_send_text),
            ('ctrl+alt+f', self.safe_send_files)
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
        """ this private method removes old hotkeys """

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

    def release_keys(self, *keys):
        for key in keys:
            try:
                keyboard.release(key)
            except:
                pass

    def reset_hotkeys(self):
        if 'manager' in globals():
            manager.stop()
            manager.start()

    def safe_send_text(self):
        self.release_keys('ctrl', 'alt', 'y')
        keyboard.unhook_all_hotkeys()
        try:
            send_text_to_linux()
        finally:
            self.start()

    def safe_send_clipboard(self):
        self.release_keys('ctrl', 'alt', 'c')
        send_clipboard()

    def safe_send_files(self):
        print("[🗃️] Files Sending Triggered: \n")
        self.release_keys('ctrl', 'alt', 'f')
        send_files_to_linux()

def main():
    global manager
    """ Main Function """
    print("[⌨] Hotkeys:")
    print("  - CTRL+ALT+C: Send Clipboard to Linux")
    print("  - CTRL+ALT+Y: Send Text to Linux")
    print("  - CTRL+ALT+F: Send Files to Linux")

    # Listening to clipboard from Linux
    Thread(target=receive_from_linux, daemon=True).start()

    # Start Hotkey Manager
    manager = HotkeyManager()
    manager.start()

    try:
        while True:
            try:
                sleep(1)
                # keep the app Always is running
            except Exception as e:  # handle any exceptions
                print(f"[!] Error: {e}")
                manager.reset_hotkeys()
                continue  # continue to the next iteration of the loop

    except KeyboardInterrupt:
        print("\n[✗] Goodbye, Client Side shutting down...")
    finally:
        manager.reset_hotkeys()
        manager.stop()

    # try:
    #     while True:
    #         sleep(1)
    # except KeyboardInterrupt:
    #     print("\n[✗] Exiting...")
    #     manager.stop()


if __name__ == "__main__":
    main()




