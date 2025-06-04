import argparse
import sys
from ast import parse
from email.policy import default

DEFAULT_IP = '127.0.0.1'
DEFAULT_PORT = 65432
class UrlSchemaRemover(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values.startswith('http://'):
            setattr(namespace, self.dest, values.replace('http://', ''))
        elif values.startswith('https://'):
            setattr(namespace, self.dest, values.replace('https://', ''))
        else:
            setattr(namespace, self.dest, values)

def parse_arguments():
    parser = argparse.ArgumentParser(description="🛜 SyncerMan Server Configuration",
                                     epilog="🤦🏼Example:\npython syncerman.py -i 192.168.10.100 -p 65432 --enable --url https://davoodya.ir --verbose" ,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-i', '--ip',
                        type=str,
                        default=DEFAULT_IP,
                        help=f"Enter IP address of the server(Default: {DEFAULT_IP})")

    parser.add_argument('-p', '--port',
                        type=int,
                        default=DEFAULT_PORT,
                        choices=range(1024, 65535),
                        metavar="1024-65535",
                        help=f"Enter port of the server(Default: {DEFAULT_PORT})")

    parser.add_argument('--url', '-u',
                        default='localhost',
                        action=UrlSchemaRemover,
                        dest='link')

    parser.add_argument('--verbose', '-v',
                        default=False,
                        action='store_true')

    parser.add_argument('--enable', action='store_true')
    parser.add_argument('--disable', action='store_false', dest='enable')
    parser.add_argument('--version', action='version', version="2.0")


    return parser.parse_args()



def main():
    args = parse_arguments()
    print(args)
    print(args.enable)
    print(args.link)
if __name__ == '__main__':
    main()
