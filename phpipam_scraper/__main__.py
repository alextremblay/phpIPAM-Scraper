import argparse
from sys import argv

from .phpipam import get_device_list

def main(keyword):
    """
    phpipam
    USAGE: phpipam [OPTIONS] KEYWORD

    DESCRIPTION: This script shows a list of all devices on phpIPAM whose hostname matches the supplied keyword

    ARGUMENTS:
        Required Args:
            KEYWORD              The IP Address of the switch you'd like to connect to.
        OPTIONS:
            -h, --help              Show this help message and quit.

    SYNOPSIS:
        This script, when run, will connect to your configured phpIPAM installation and poll the devices list for
        any device whose hostname matches the keyword provided.
    """

    results = get_device_list(keyword)
    for result in results:
        print('Name: {0}  ||  IP: {1}'.format(result[0], result[1]))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('KEYWORD')

    # Print help if no arguments given, otherwise run the script
    if len(argv) < 2 or argv[1] == '-h' or argv[1] == '--help':
        print(main.__doc__)
    else:
        args = parser.parse_args()
        main(args.KEYWORD)