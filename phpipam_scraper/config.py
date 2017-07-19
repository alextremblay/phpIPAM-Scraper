"""
phpIPAM Scraper Config Module

The purpose of this module is to store and retrieve configuration info for 
the phpIPAM Scraper package. We want to store the URL of the phpIPAM 
installation to connect to, as well as optionally storing a username and 
password for said installation for scripting purposes.

The configuration info should be stored in one of two places: a system-wide 
configuration file, and a user-specific configuration file. The system-wide 
file is optional. 
If there is no system-wide config file, then a user-specific file is mandatory 
and must be generated if it does not already exist. If there is a system-wide 
config file, then the user-specific file should be treated as an optional 
override.
"""

import os
import sys
from configparser import ConfigParser
from getpass import getpass

PY2 = sys.version_info[0] == 2
OS = sys.platform
if PY2:
    # noinspection PyUnresolvedReferences
    input = raw_input

FS_ROOT = 'C:' if OS is 'win32' else '/'
USER_DIR = os.path.expanduser('~')
SYSTEM_FILE = os.path.join(FS_ROOT, 'etc', 'phpipam', 'config')
USER_FILE = os.path.join(USER_DIR, '.config', 'phpipam', 'config')


def load_config(executed_before=False):
    parser = ConfigParser()
    # Let's read in a list of all the config files we want, and track how
    # many of them succeeded in being read
    user_file_mandatory = False
    try:
        with open(SYSTEM_FILE) as sys_file:
            parser.read_file(sys_file)
    except FileNotFoundError:
        user_file_mandatory = True
    try:
        with open(USER_FILE) as user_file:
            parser.read_file(user_file)
    except FileNotFoundError:
        if user_file_mandatory:
            # We were unable to load either the system-wide config or the
            # user config.
            if executed_before:
                # If we've run this function before and still can't find valid
                # configs, then something has gone wrong.
                raise Exception(
                    "Something has gone wrong. Unable to verify the "
                    "configuration file that was just created. Please "
                    "verify the existence and permissions of"
                    + USER_FILE)
            else:
                # Looks like we'll need to generate new config info
                # and try again.
                get_new_config()
                return load_config(executed_before=True)

        else:
            pass

    # We now have our config data loaded and are ready to pass it on to the
    # client
    config_data = {
        "URL": parser['main']['URL'],
        "User": parser.get('main', 'User', fallback=None),
        "Pass": parser.get('main', 'Pass', fallback=None)
    }

    return config_data


def get_new_config():
    print("It seems your phpIPAM Scraper installation is not yet configured "
          "for use. Please answer the following questions to configure "
          "phpIPAM Scraper:")
    parser = ConfigParser()
    parser['main'] = {}  # Initialize the 'main' section of the config
    url = input('phpIPAM URL: ')
    # Add in the protocol specifier if it isn't already there
    if 'http' not in url[:4]:
        url = 'http://' + url
    # take out the trailing slash, we'll add it back in later
    url = url.rstrip('/')

    parser['main']['URL'] = url
    username = input('phpIPAM Username (Optional. Press Enter to skip): ')
    if len(username) is not 0:
        parser['main']['User'] = username

    password = getpass('phpIPAM Password (Optional. Press Enter to skip): ')
    if len(password) is not 0:
        parser['main']['Pass'] = password

    print("Thank you for providing the requested information. If you are "
          "ready to proceed, please press 'y'. If you have made an error and "
          "wish to start over, press any other key")
    response = input("Proceed? ")
    if 'y' in response:
        try:
            assure_path_exists(USER_FILE)
            with open(USER_FILE, 'w') as file:
                parser.write(file)
            print("Configuration data successfully saved to " + USER_FILE +
                  ". If you would like to make this configuration globally "
                  "accessible to all users on your system, please copy it to "
                  + SYSTEM_FILE)
        except PermissionError:
            red_color = '\033[91m'
            no_color = '\033[0m'
            sys.exit(
                red_color + "Error: Unable to save configuration. Please "
                "ensure that you have permission to write to " + USER_FILE +
                " and to create this folder path if it doesn't exist" + no_color
            )
    else:
        get_new_config()


def assure_path_exists(path):
    folder = os.path.dirname(path)
    if not os.path.exists(folder):
        os.makedirs(folder)


config = load_config()
