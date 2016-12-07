import os
import sys
import re
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
    if re.match(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)', url):
        config.set('phpipam', 'url', url)
    else:
        raise Exception('Invalid URL specified. ' + url + 'does not appear to be a Fully Qualified Domain Name.')
    for path in paths:
        try:
            os.makedirs(os.path.dirname(path))
        except OSError:
            pass
    writeable_paths = filter(lambda item: os.access(item, os.W_OK), paths)
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
    print('phpIPAM configuration not found: Please enter the URL for your phpIPAM installation')
    print('Example: http://ipam.yourcompanyaddress.com or http://yourwebsite.com/phpipam')
    url = raw_input('phpIPAM URL:').rstrip('/')
    set_url(url)


def show_config_paths():
    for path in paths:
        print(os.access(path, os.W_OK), path)
