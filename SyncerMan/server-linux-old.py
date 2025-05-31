import socket
import keyboard
from time import sleep
from pyperclip import copy, paste
from threading import Thread, Event
from settings import WINDOWS_CLIENT_IP, CLIENT_RECEIVE_PORT

last_clipboard = ""

""" Section 3: Handle the received Data from Windows Client """
def handle_client(conn, addr):
    """ this function handling received data from the Windows client """

    # Step 0: Receive data from the Windows client
    data = conn.recv(4096)

    # Step 1: Decode the received data
    try:
        decoded = data.decode("utf-8")
    except Exception as e:
        decoded = f"[✗] Could not decode clipboard content. Error: {e}"

    # Step 2: Write received data to a file
    with open("PC_Received.txt", "a", encoding="utf-8") as file:
        file.write(decoded + "\n\n")

    # Step 3: Copy the received data to the clipboard
    copy(decoded)
    print("[✓] Data written to PC_Received.txt and copied to clipboard.")
    print(f':: Data: {decoded}')

    # Step 4: Close Connection
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

            if data == paste():
                print("[✓] Sent clipboard to Windows.")
                last_clipboard = data
            else:
                print(f"[✓] Sent {data} to Windows.")

        except Exception as e:
            print(f"[✗] Could not send to Windows: {e}")
    else:
        print("[✓] Clipboard Unchanged, not sent.")

""" Section 10: Define send_text Callback function for sending input texts to windows"""
def send_text_to_windows(callback, data=''):
    data = ''
    data = input("enter text: ")
    callback(data=data)

def send_text(data=''):
    data = input("enter text: ")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((WINDOWS_CLIENT_IP, CLIENT_RECEIVE_PORT))
            s.sendall(data.encode("utf-8"))
            print(f"[✓] Sent {data} to Windows.")
    except Exception as e:
        print(f"[✗] Could not send to Windows: {e}")

""" Section 11: Define Add Hotkeys"""
# def refresh_hotkeys():
#     keyboard.unhook_all_hotkeys()
#     keyboard.add_hotkey('ctrl+shift+v', send_clipboard_to_windows)
#     keyboard.add_hotkey('ctrl+shift+y', lambda: send_text(send_clipboard_to_windows))
""" Section 8: Add Hotkeys Class """
# class HotkeyManager:
#     def __init__(self):
#         self.exit_event = Event()
#         self.hotkeys = [
#             ('ctrl+shift+v', send_clipboard_to_windows),
#             ('ctrl+shift+y', lambda: send_text_to_windows(send_clipboard_to_windows))
#         ]
#         self.registered_ids = []
#
#
#     def start(self):
#         """ Register Hotkeys & Start Hotkey System """
#         # 1. Clear old hotkeys
#         self._cleanup()
#
#         # 2. Register new hotkeys
#         for hotkey, callback in self.hotkeys:
#             hotkey_id = keyboard.add_hotkey(hotkey, callback)
#             self.registered_ids.append(hotkey_id)
#
#         # 3. Start Hotkey Listener
#         Thread(target=self._listener_thread, daemon=True).start()
#
#
#     def _cleanup(self):
#         """this private method removes old hotkeys """
#
#         # 1. Iterate on all registered hotkeys, then remove them
#         for hotkey_id in self.registered_ids:
#             try:
#                 keyboard.remove_hotkey(hotkey_id)
#             except:
#                 pass
#         # 2. Clear the list of registered hotkeys
#         self.registered_ids.clear()
#
#
#     def _listener_thread(self):
#         """ Main Thread for keeping the program running """
#         while not self.exit_event.is_set():
#             keyboard.wait()
#             sleep(0.1)  # Prevent high CPU usage
#
#     def stop(self):
#         """ this function Stop the system """
#         self.exit_event.set()
#         self._cleanup()


def main():
    print("[⌨] Hotkeys:")
    print("  - CTRL+SHIFT+V: Send Clipboard to Windows")
    print("  - CTRL+SHIFT+Y: Send Text to Windows")

    """ Section 12: Start Server Receiver using Multithreading  """
    Thread(target=start_receive_server, daemon=True).start()

    while True:
        if keyboard.is_pressed('ctrl+shift+v'):
            send_clipboard_to_windows()
            sleep(0.1)
        if keyboard.is_pressed('ctrl+shift+u'):
            send_text_to_windows(send_clipboard_to_windows)
            sleep(0.1)



if __name__ == "__main__":
    main()