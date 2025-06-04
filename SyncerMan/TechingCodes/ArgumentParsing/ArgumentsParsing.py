import argparse
import sys
from ast import parse

DEFAULT_IP = '127.0.0.1'
DEFAULT_PORT = 65432

def parse_arguments():
    parser = argparse.ArgumentParser(description="SyncerMan Server Configuration",
                                     epilog="Example:\npython syncerman.py -i 192.168.10.100 -p 65432",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-i', '--ip',
                        type=str,
                        default=DEFAULT_IP,
                        help=f"Enter IP address of the server")

    parser.add_argument('-p', '--port',
                        type=int,
                        default=DEFAULT_PORT,
                        choices=range(1024, 65535),
                        metavar="1024-65535",
                        help=f"Enter port of the server")

    return parser.parse_args()

def main():
    args = parse_arguments()
    ip = args.ip
    port = args.port

    print(f"IP: {ip} & Port: {port}")

if __name__ == '__main__':
    main()
