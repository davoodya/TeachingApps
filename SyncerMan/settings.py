"""
This tool written by Yakuza.D; Hello Ninja, Use it and Enjoy...
Notes:
    1. You should define Allow Firewall Specially for windows (Incoming on 65432, 65433)
    2. If on Linux server using Firewall, you should define allow rule for port 65432 and 65433

"""

""" Section 0: Define Global Variables """

""" Variables for Client (Windows) """
SERVER_IP = "192.168.10.78"  # Linux Server IP address

SERVER_PORT = 65432 # Linux Server Listening Port
# Note: SERVER_PORT should be the same as server side in start_receive_server(port=65432)


""" Variables for Server (Linux) """
WINDOWS_CLIENT_IP = "192.168.10.100" # Windows Client IP address


""" Variables for Both Client & Server Sides (Windows and Linux) """
CLIENT_RECEIVE_PORT = 65433 # Windows Client Port for receiving from Windows (Bidirectional Synchronization)