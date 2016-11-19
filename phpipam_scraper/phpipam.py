from time import time
import cookielib
import os
import getpass

from .config import get_url_from_config_file
import clint
import requests  # External module requests
from bs4 import BeautifulSoup  # External module BeautifulSoup4


DEVICE_URL_PATH = '/app/tools/devices/devices-print.php'
AUTH_URL_PATH = '/app/login/login_check.php'


class IPAM(object):

    def __init__(self, username, password, url=None):
        self._username = username
        self._password = password
        self._url = url if url else get_url_from_config_file()
        self.session = requests.session()

    def get_device_list(self, keyword):
        if self.auth_cookie.is_expired():
            self.auth_cookie = self._get_auth_cookie()

    def _get_auth_cookie(self):
        auth = dict()
        auth['ipamusername'] = raw_input('PHPIPAM Username:')
        auth['ipampassword'] = getpass.getpass('PHPIPAM Password:')
        response = requests.post(self._url + AUTH_URL_PATH, data=auth)
        if 'Invalid username' in response.content:
            raise Exception('PHPIPAM error: Invalid username or password')
        token = response.cookies['phpipam']
        expires = time() + 1800
        attr = {'version': 0, 'port': None, 'port_specified': None, 'domain': '', 'domain_specified': False,
                'domain_initial_dot': None, 'path': '/', 'path_specified': False, 'secure': None, 'discard': None,
                'comment': '', 'comment_url': '', 'rest': {}}
        auth_cookie = cookielib.Cookie(name='phpipam', value=token, expires=expires, **attr)

