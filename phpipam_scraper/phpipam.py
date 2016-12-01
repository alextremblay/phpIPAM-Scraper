# Python Standard Library imports
import getpass
import re

# Internal Module imports
from .config import get_url

# External Package imports
import requests
from bs4 import BeautifulSoup  # Package name: BeautifulSoup4


class IPAM(object):

    def __init__(self, username=None, password=None, url=None):
        self._username = username
        self._password = password
        self._url = url if url else get_url()
        self._device_url_path = self._url + '/app/tools/devices/devices-print.php'
        self._search_url_path = self._url + '/app/tools/search/search-results.php'
        self._auth_url_path = self._url + '/app/login/login_check.php'
        self.session = requests.session()
        self.login()

    def get_from_devices(self, keyword):
        search_parameters = {'ffield': 'hostname', 'fval': keyword, 'direction': 'hostname|asc'}
        soup = self.get_page(self._device_url_path, search_parameters)
        device_table = soup.find('table', id='switchManagement')
        result = []
        # Get all table rows
        for row in device_table.find_all('tr'):
            # Get all cells in each table row
            columns = row.find_all('td')
            # Only process rows containing <td> cells.
            # Rows without <td> cells, like the header row at the top of the
            # table, are ignored
            if len(columns) > 0:
                # If phpipam doesn't have any results for a given search,
                # the first non-header row will contain a single <td> cell with a warning message in it.
                # If we find that, we should break the loop and return an empty
                # list
                if 'No devices configured!' in str(columns[0]):
                    break
                # Only rows that have an <a> tag in the first column are devices. Rows that have a blank field
                # instead of an ip address in column[1] are of no interest to us.
                hostname = columns[0].a
                ip_address = columns[1]
                if len(ip_address) > 0 and hostname:
                    result.append((hostname.text, ip_address.text))
        return result


    def get_from_search(self, keyword):
        search_parameters = {'ip': keyword, 'addresses': 'on', 'subnets': 'off', 'vlans': 'off', 'vrf': 'off'}
        soup = self.get_page(self._search_url_path, search_parameters)
        table_rows = soup.find_all('tr', class_='ipSearch')

        address_array = []
        for tr in table_rows:
            row = []
            for td in tr.find_all('td'):
                row.append(td.get_text())
            address_array.append(row)
        address_array = [[row[2], row[0]] for row in address_array if re.match(keyword, row[2])]
        return address_array


    def login(self):
        auth = self.get_credentials()
        response = self.session.post(self._auth_url_path, data=auth)
        if 'Invalid username' in response.content:
            print('PHPIPAM error: Invalid username or password. Please try again')
            self._username = None
            self._password = None
            self.login()


    def get_page(self, url, post_data):
        page = self.session.post(url, data=post_data)
        if page.status_code == 404:
            raise Exception('Woops! We made contact with the server you configured, but received a "Page Not Found" '
                            'error from it. Please double-check your configured phpIPAM URL by running '
                            '"phpipam get-url" or "phpipam set-url" from your command line.')
        soup = BeautifulSoup(page.content, 'html.parser')
        # If the page has a <div id="login"> tag in it, that means our session token is expired. We need to
        # re-authenticate and try again
        if soup.find('div', id='login'):
            print('Your login to phpIPAM has expired. Please log in now.')
            self.login()
            self.get_page(url, post_data)
        # If no <div id="login">, then we are still logged in and may proceed
        else:
            return soup


    def get_credentials(self):
        auth = dict()
        if not self._username:
            self._username = raw_input('phpIPAM Username:')
        auth['ipamusername'] = self._username
        if not self._password:
            self._password = getpass.getpass('phpIPAM Password:')
        auth['ipampassword'] = self._password
        return auth
