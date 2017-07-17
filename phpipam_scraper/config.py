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


def main(executed_before=False):
    config = ConfigParser()
    # Let's read in a list of all the config files we want, and track how
    # many of them succeeded in being read
    succeeded = config.read(SYSTEM_FILE, USER_FILE)

    if len(succeeded) is 0:
        # There is no configuration information on this system
        if executed_before:
            # Something is wrong. We've run the main function twice and still
            #  don't have valid configuration data. We need to bail now
            # before we get stuck in an infinite loop
            raise Exception("Something went wrong. Unable to retrieve "
                            "configuration information from your system. "
                            "Please submit an issue for this at "
                            "https://github.com/alextremblay/phpipam-scraper")
        # Generate configuration data to populate the user config file, then
        # try again
        get_new_config()
        main()

    config_data = {
        "URL": config['main']['URL'],
        "User": config.get('main', 'User', fallback=None),
        "Pass": config.get('main', 'Pass', fallback=None)
    }

    return config_data


def get_new_config():
    print("It seems your phpIPAM Scraper installation is not yet configured "
          "for use. Please answer the following questions to configure "
          "phpIPAM Scraper:")
    config = ConfigParser()
    url = input('phpIPAM URL: ')
    if url[:4] is not 'http':
        url = 'http://'+url

    # take out the trailing slash, we'll add it back in later
    url = url.rstrip('/')

    config['main'][url] = url
    username = input('phpIPAM Username (Optional. Press Enter to skip): ')
    if len(username) is not 0:
        config['main']['User'] = username
    password = getpass('phpIPAM Password (Optional. Press Enter to skip): ')
    if len(password) is not 0:
        config['main']['Pass'] = password

    print("Thank you for providing the requested information. If you are "
          "ready to proceed, please press 'y'. If you have made an error and "
          "wish to start over, press any other key")
    if input("proceed? ") is 'y':
        assure_path_exists(USER_FILE)
        config.write(USER_FILE)
    else:
        get_new_config()


def assure_path_exists(path):
    folder = os.path.dirname(path)
    if not os.path.exists(folder):
        os.makedirs(folder)


main()
