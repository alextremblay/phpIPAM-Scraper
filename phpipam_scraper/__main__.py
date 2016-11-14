"""
    phpipam
    USAGE: phpipam [OPTIONS] KEYWORD

    DESCRIPTION: This script shows a list of all devices on phpIPAM whose hostname matches the supplied keyword

    ARGUMENTS:
        Required Args:
            KEYWORD              The IP Address of the switch you'd like to connect to.
        OPTIONS:
            -r                      Reset phpIPAM configuration file
            -h, --help              Show this help message and quit.

    SYNOPSIS:
        This script, when run, will connect to your configured phpIPAM installation and poll the devices list for
        any device whose hostname matches the keyword provided.
"""
import argparse
from sys import argv

from tabulate import tabulate
from .phpipam import get_device_list, setup_config


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('KEYWORD')

    # Print help if no arguments given, otherwise run the script
    if len(argv) < 2 or argv[1] == '-h' or argv[1] == '--help':
        print(__doc__)  # Prints the module docstring at the start of this file
    elif argv[1] == '-r':
        setup_config()
    else:
        args = parser.parse_args()
        results = get_device_list(args.KEYWORD)
        print(tabulate(results, headers=['Hostname', 'IP Address']))

if __name__ == '__main__':
    main()
