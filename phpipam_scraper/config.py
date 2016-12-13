import os
import sys
import re
from configparser import ConfigParser, NoOptionError

import requests

if sys.platform == 'win32':
    paths = [
        os.path.join(os.getenv('LOCALAPPDATA'), 'phpipam', 'phpipam.cfg'),
        os.path.join(os.path.dirname(__file__), 'phpipam.cfg')
    ]
else:
    paths = [
        os.path.join('/', 'usr', 'local', 'phpipam.cfg'),
        os.path.expanduser('~/.local/phpipam.cfg'),
        os.path.join(os.path.dirname(__file__), 'phpipam.cfg')
    ]

config = ConfigParser()
config.add_section('phpipam')


def get_url():
    """

    Retrieves stored URL from a configuration file stored in one of 3 locations on the system. See the paths variable
    in phpipam_scraper.config for details on where this file is stored

    :return: URL of the phpIPAM site to connect to
    :rtype: str or Exception
    """
    try:
        config.read(paths)
        return config.get('phpipam', 'url')
    except NoOptionError:
        first_time_setup()
        config.read(paths)
        return config.get('phpipam', 'url')


def set_url(url):
    """

    Set URL for phpIPAM site to connect to, and store variable in a onfiguration file stored in one of 3 locations on
    the system. See the paths variable in phpipam_scraper.config for details on where this file is stored

    :param url: URL of the phpIPAM site to connect to
    :type url: str
    :return: True on success, Exception on failure
    :rtype: bool or Exception
    """
    if _is_a_website(url) and _is_a_phpipam_site(url):
        config.set('phpipam', 'url', url)
    else:
        sys.tracebacklimit = 0
        raise Exception(url + ' does not appear to be a valid phpIPAM installation. Please check the URL and try again')
    for path in paths:
        try:
            os.makedirs(os.path.dirname(path))
        except OSError:
            pass
    writeable_paths = [path for path in paths if os.access(path, os.W_OK)]
    if len(writeable_paths) == 0:
        path_list = ''
        for path in paths:
            path_list += str(path) + '\n'
        raise Exception('No viable path available to save configuration file. \n'
                        'Please ensure you have write access to at least one of these file paths: \n' + path_list)
    else:
        with open(paths[0], 'w') as f:
            config.write(f)
            return True


def first_time_setup():
    """

    If an attempt is make to retireve the phpIPAM URL from store config file, but no stored config file exists, this
    function is called to prompt the user for a URL to store, and sets the URL received from the user

    """
    print('phpIPAM configuration not found: Please enter the URL for your phpIPAM installation')
    print('Example: http://ipam.yourcompanyaddress.com or http://yourwebsite.com/phpipam')
    url = raw_input('phpIPAM URL:').rstrip('/')
    set_url(url)


def _is_a_website(url):
    return re.match(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)', url)


def _is_a_phpipam_site(url):
    resp = requests.get(url + '/app/login/login_check.php')
    if resp.status_code == 200:
        return True
    else:
        return False


def _show_config_paths():
    for path in paths:
        print(os.access(path, os.W_OK), path)
