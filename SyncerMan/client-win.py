import socket
from threading import Thread
from pyperclip import copy, paste
from settings import SERVER_IP, SERVER_PORT, CLIENT_RECEIVE_PORT

last_clipboard = ""

""" Section 1: Send Clipboard to Linux Server """
def send_clipboard(text="1"):
    # Step 1: Get clipboard data if not argument is passed
    if text == "1":
        text = paste()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((SERVER_IP, SERVER_PORT))
            sock.sendall(text.encode("utf-8"))
        print("[✓] Sent clipboard to Linux.")
    except Exception as e:
        print(f"[✗] Error sending clipboard to Linux: {e}")

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
        print(f"[🔗] Connection established from {addr}")
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

    print(f"[✓] Data Received from {addr}\n::Written to Linux_Received.txt and copied to clipboard.")

    # Step 4: Close Connection
    conn.close()


if __name__ == "__main__":
    receive_from_linux()


