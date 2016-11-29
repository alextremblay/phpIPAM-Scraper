import os
import sys
from ConfigParser import ConfigParser, NoOptionError

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
    config.read(paths)
    try:
        return config.get('phpipam', 'url')
    except NoOptionError:
        first_time_setup()
        config.read(paths)
        return config.get('phpipam', 'url')


def set_url(url):
    config.set('phpipam', 'url', url)
    for path in paths:
        try:
            os.makedirs(os.path.dirname(path))
        except OSError:
            pass
        try:
            with open(path, 'w') as f:
                config.write(f)
        except (IOError, OSError):
            pass


def first_time_setup():
    print('phpIPAM configuration not found: Please enter the URL for your phpIPAM installation')
    print('Example: http://ipam.yourcompanyaddress.com or http://yourwebsite.com/phpipam')
    url = raw_input('phpIPAM URL:').rstrip('/')
    set_url(url)


def show_config_paths():
    for path in paths:
        print(os.access(path, os.W_OK), path)
