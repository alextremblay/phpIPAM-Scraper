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

FS_ROOT = 'C:' if OS is 'win32' else '/'
USER_DIR = os.path.expanduser('~')
SYSTEM_FILE = os.path.join(FS_ROOT, 'etc', 'phpipam', 'config')
USER_FILE = os.path.join(USER_DIR, '.config', 'phpipam', 'config')


# These are the variable that users of our module will use
url = None
username = None
password = None


def load_config(executed_before=False):
    # This function alters global variables. Let's put this up here so it's
    # easy to see
    global url
    global username
    global password

    parser = ConfigParser()
    # Lets read in the system config file, then tyhe user config file. If the
    # system config file doesn't exist, then we MUST successfully read the
    # user config file or create a new one
    user_file_mandatory = False
    try:
        with open(SYSTEM_FILE) as sys_file:
            parser.read_file(sys_file)

        # We now have our config data loaded and are ready to commit it
        # to module memory
        url = parser.get('main', 'URL', fallback=None)
        username = parser.get('main', 'User', fallback=None)
        password = parser.get('main', 'Pass', fallback=None)

    except (FileNotFoundError, PermissionError):
        user_file_mandatory = True
    try:
        with open(USER_FILE) as user_file:
            parser.read_file(user_file)

        username = parser.get('main', 'User', fallback=None)
        password = parser.get('main', 'Pass', fallback=None)
        if user_file_mandatory:
            # If there is no system config file, and the user config file
            # does not contain a URL entry, then we should fail and generate
            # a new config file.
            url = parser['main']['URL']
        else:
            # If there was a system config file found, then the URL entry in
            # the user config file should be considered optional and
            # supplementary
            if parser.has_option('main', 'URL'):
                url = parser['main']['URL']

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

        else:
            pass



def get_new_config():
    print("It seems your phpIPAM Scraper installation is not yet configured "
          "for use. Please answer the following questions to configure "
          "phpIPAM Scraper:")
    parser = ConfigParser()
    parser['main'] = {}  # Initialize the 'main' section of the config
    new_url = _get_input('phpIPAM URL: ')
    # Add in the protocol specifier if it isn't already there
    if 'http' not in new_url[:4]:
        new_url = 'http://' + new_url
    # take out the trailing slash, we'll add it back in later
    new_url = new_url.rstrip('/')

    parser['main']['URL'] = new_url
    new_username = _get_input('phpIPAM Username '
                              '(Optional. Press Enter to skip): ')
    if len(new_username) is not 0:
        parser['main']['User'] = new_username

    new_password = _get_pass('phpIPAM Password '
                             '(Optional. Press Enter to skip): ')
    if len(new_password) is not 0:
        parser['main']['Pass'] = new_password

    print("Thank you for providing the requested information. If you are "
          "ready to proceed, please press 'y'. If you have made an error and "
          "wish to start over, press any other key")
    response = _get_input("Proceed? ")
    if 'y' in response:
        try:
            _assure_path_exists(USER_FILE)
            with open(USER_FILE, 'w') as file:
                parser.write(file)
            print("Configuration data successfully saved to:\n" + USER_FILE +
                  "\nIf you would like to make this configuration globally "
                  "accessible to all users on your system, please copy it to:\n"
                  + SYSTEM_FILE)
            load_config(executed_before=True)
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


def _assure_path_exists(path):
    folder = os.path.dirname(path)
    if not os.path.exists(folder):
        os.makedirs(folder)


def _get_input(prompt):
    if PY2:
        # noinspection PyUnresolvedReferences
        return raw_input(prompt)
    else:
        return input(prompt)


def _get_pass(prompt):
    return getpass(prompt)
