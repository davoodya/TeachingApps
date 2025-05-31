import socket
from threading import Thread, Event
from time import sleep
import keyboard
from pyperclip import copy, paste
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
def send_text(callback, text=''):
    text = input("enter text: ")
    callback(text)

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
    # Step 0: Receive data from the Linux server
    data = conn.recv(4096)

    # Step 1: Decode the received data
    decoded = data.decode("utf-8")

    # Step 2: Write received data to a file
    with open("Linux_Received.txt", "a", encoding="utf-8") as file:
        file.write(decoded + "\n\n")

    # Step 3: Copy the received data to the clipboard
    copy(decoded)

    print(f"[✓] Data Written to Linux_Received.txt and copied to clipboard.")
    print(f':: Data: {decoded}')

    # Step 4: Close Connection
    conn.close()



# keyboard.add_hotkey('ctrl+alt+c', send_clipboard)
# keyboard.add_hotkey('ctrl+alt+y', lambda: send_text(send_clipboard))

""" Section 8: Add Hotkeys Class """
class HotkeyManager:
    def __init__(self):
        self.exit_event = Event()
        self.hotkeys = [
            ('ctrl+alt+c', send_clipboard),
            ('ctrl+alt+y', lambda: send_text(send_clipboard))
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

def main():
    """ Main Function """
    print("[⌨] Hotkeys:")
    print("  - CTRL+ALT+C: Send Clipboard to Linux")
    print("  - CTRL+ALT+Y: Send Text to Linux")

    # Listening to clipboard from Linux
    Thread(target=receive_from_linux, daemon=True).start()

    # Start Hotkey Manager
    manager = HotkeyManager()
    manager.start()

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        manager.stop()

if __name__ == "__main__":
    main()




