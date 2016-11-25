import os
import sys

if sys.platform == 'win32':
    paths = [
        os.path.join(os.getenv('LOCALAPPDATA'), 'phpipam', 'phpipam.cfg')
    ]
else:
    paths = [
        os.path.join('/', 'usr', 'local', 'phpipam.cfg'),
        os.path.expanduser('~/.local/phpipam.cfg')
    ]

error = None


def get_url_from_config_file():
    if check(sys_path):
        return read(sys_path)
    elif check(user_path):
        return read(user_path)
    elif create_config_file(sys_path):
        return read(sys_path)
    elif create_config_file(user_path):
        return read(user_path)
    else:
        raise Exception('Failed to save phpIPAM configuration. \n'
                        'Attempted to write to the following directories: \n'
                        + sys_path + '\n'
                        + user_path + '\n'
                        + 'Please verify your file write permissions and try again.')

def create_config_file(file_path):
    try:
        os.makedirs(os.path.dirname(file_path))
        log('PHPIPAM configuration not found! Please enter the URL for your PHPIPAM installation')
        log('Example: http://ipam.yourcompanyaddress.com or http://yourwebsite.com/phpipam')
        url = get_input('PHPIPAM URL:').rstrip('/')
        write(file_path, url)
        log('Configuration saved successfully!')
        return True
    except OSError as e:
        log('Failed to write configuration to ' + file_path)
        global error
        error = e.message
        return False


def read(file_path):
    with open(file_path) as f:
        return f.read()


def write(file_path, data):
    with open(file_path, 'w') as f:
        f.write(data)


def check(file_path):
    return os.path.isfile(file_path)


def log(*args):
    print(args)


def get_input(prompt):
    return raw_input(prompt)





