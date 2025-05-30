import socket
import keyboard
from pyperclip import copy, paste
from threading import Thread
from settings import WINDOWS_CLIENT_IP, CLIENT_RECEIVE_PORT

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
    """ this function sends clipboard data from linux server to the Windows client """
    # Step 1: Get clipboard data if not argument is passed
    if data == "1":
        data = paste()

    # Step 2: Check if clipboard is empty don't send it
    if not data.strip():
        print("[!] Clipboard is empty. Nothing to send.")
        return
    # Step 3: Send clipboard data to the Windows client
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((WINDOWS_CLIENT_IP, CLIENT_RECEIVE_PORT))
            s.sendall(data.encode("utf-8"))
        if data == paste():
            print("[✓] Sent clipboard to Windows.")
        else:
            print(f"[✓] Sent {data} to Windows.")

    except Exception as e:
        print(f"[✗] Could not send to Windows: {e}")

""" Section 10: Define send_text Callback function for sending input texts to windows"""
def send_text(callback, text=''):
    text = input("enter text: ")
    callback(text)


""" Section 11: Define Add Hotkeys"""
keyboard.add_hotkey('ctrl+shift+v', send_clipboard_to_windows)
keyboard.add_hotkey('ctrl+shift+y', lambda: send_text(send_clipboard_to_windows))


if __name__ == "__main__":
    print("[⌨] Hotkeys:")
    print("  - CTRL+SHIFT+V: Send Clipboard to Windows")
    print("  - CTRL+SHIFT+Y: Send Text to Windows")

    """ Section 12: Start Server Receiver using Multithreading  """
    Thread(target=start_receive_server, daemon=True).start()

    while True:
        keyboard.wait()