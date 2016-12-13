# Python Standard Library imports
import getpass
import re

# Internal Module imports
from .config import get_url

# External Package imports
import requests
from bs4 import BeautifulSoup  # Package name: BeautifulSoup4
from bs4.element import Tag


class IPAM(object):
    def __init__(self, username=None, password=None, url=None):
        """

        The main class for this entire project. Stores all information related to a connection to a give phpIPAM
        installation. During initialization, it will prompt for username and password if one is not supplied, and will
        attempt to retrieve the URL for the phpIPAM installation from a config file if a URL is not specified. It will
        then attempt to login and open a persistent session to process future requests.

        :param username: The username for your phpIPAM account
        :type username: str or None
        :param password: The password  for your phpIPAM account
        :type password: str or None
        :param url: The URL to connect to
        :type url: str or None
        """
        self._username = username
        self._password = password
        self._url = url if url else get_url()
        self._device_url_path = self._url + '/app/tools/devices/devices-print.php'
        self._search_url_path = self._url + '/app/tools/search/search-results.php'
        self._auth_url_path = self._url + '/app/login/login_check.php'
        self.session = requests.session()
        self._login()

    def get_from_devices(self, keyword):
        """

        Retrieves device information from phpIPAM's devices page

        :param keyword: keyword to search by
        :type keyword: str
        :return: list of dicts containing hostname, IP, and description for each device found
        :rtype: list(dict)
        """
        search_parameters = {'ffield': 'hostname', 'fval': keyword, 'direction': 'hostname|asc'}
        soup = self._get_page(self._device_url_path, search_parameters)
        device_table = soup.find('table', id='switchManagement')
        table_headers = ['Hostname', 'IP Address', 'Description', 'hosts', 'type', 'vendor', 'model', 'actions']
        result = self._convert_to_dictionary(device_table, table_headers)
        good_keys = ['IP Address', 'Description', 'Hostname']
        result = self._filter_keys(result, good_keys)
        result = self._filter_by_ip(result)
        return result

    def get_from_search(self, keyword):
        """

        Retrieves device information from phpIPAM's search page

        :param keyword: keyword to search by
        :type keyword: str
        :return: list of dicts containing hostname, IP, and description for each device found
        :rtype: list(dict)
        """
        search_parameters = {'ip': keyword, 'addresses': 'on', 'subnets': 'off', 'vlans': 'off', 'vrf': 'off'}
        soup = self._get_page(self._search_url_path, search_parameters)
        table_rows = soup.find_all('tr', class_='ipSearch')
        table_headers = ['IP Address', 'Description', 'Hostname', 'other', 'device', 'port', 'owner', 'note', 'actions']
        result = self._convert_to_dictionary(table_rows, table_headers)
        good_keys = ['IP Address', 'Description', 'Hostname']
        result = self._filter_keys(result, good_keys)
        result = self._filter_by_ip(result)
        return result

    def get_all(self, keyword):
        """

        Calls self.get_from_search and self.get_from_device together, combines their results, tags each entry with a \
        source to denote where it came from

        :param keyword: keyword to search by
        :type keyword: str
        :return: list of dicts containing hostname, IP, description, and source for each device found
        :rtype: list(dict)
        """
        dev_results = self.get_from_devices(keyword)
        for item in dev_results:
            item['Source'] = "phpIPAM Device Page"
        search_results = self.get_from_search(keyword)
        for item in search_results:
            item['Source'] = "phpIPAM Search Page"
        return dev_results + search_results

    def _login(self):
        """

        Logs in to phpIPAM using stored credentials, checks for failure, tries again until success

        """
        auth = self._get_credentials()
        response = self.session.post(self._auth_url_path, data=auth)
        if 'Invalid username' in response.text:
            print('PHPIPAM error: Invalid username or password. Please try again')
            self._username = None
            self._password = None
            self._login()

    def _get_credentials(self):
        """

        Checks to see if phpIPAM username / password are defined, prompts user for input if they are not.

        :return: a dictionary containing username / password, formatted to be posted to phpIPAM's login page
        """
        auth = dict()
        if not self._username:
            self._username = raw_input('phpIPAM Username:')
        auth['ipamusername'] = self._username
        if not self._password:
            self._password = getpass.getpass('phpIPAM Password:')
        auth['ipampassword'] = self._password
        return auth

    def _get_page(self, url, post_data):
        """

        Given a URL, and a dictionary of data to post to the URL, this function will send the requested data to that
        URL, download the resulting page, convert it into a beautiful soup object, and return it

        :param url: URL to post to
        :type url: str
        :param post_data: dict of key / value pairs to post to the URL
        :return: BeautifulSoup object
        """
        page = self.session.post(url, data=post_data)
        if page.status_code == 404:
            raise Exception('Woops! We made contact with the server you configured, but received a "Page Not Found" '
                            'error from it. Please double-check your configured phpIPAM URL by running '
                            '"phpipam get-url" or "phpipam set-url" from your command line.')
        soup = BeautifulSoup(page.text, 'html.parser')

        # If the page has a <div id="login"> tag in it, that means our session token is expired. We need to
        # re-authenticate and try again
        if soup.find('div', id='login'):
            print('Your login to phpIPAM has expired. Please log in now.')
            self._login()
            self._get_page(url, post_data)

        # If no <div id="login">, then we are still logged in and may proceed
        else:
            return soup

    @staticmethod
    def _convert_to_dictionary(soup, keys):
        """

        Converts a bs4 soup html table into a list of dictionaries.

        :param soup: bs4 soup object holding an html table
        :param keys: list of strings to represent keys for the dictionaries; <td> cells in the table will be mapped to
            these keys in the order they are found
        :return: list of dicts
        """
        address_array = []
        for tr in soup:
            # This variable will hold all the information we  gather from a given row of the supplied HTML table
            entry = {}
            # Some rows are empty, and only hold a newline character. We want to skip those
            if type(tr) is not Tag:
                continue

            # Grab all the cells from a row
            tds = tr.find_all('td')

            # Ignore rows that don't match the profile we've been given
            if len(tds) != len(keys):
                continue

            # Map the text in each cell into a key in our 'entry' dictionary, using the 'keys' list provided
            for index, td in enumerate(tds):
                value = td.get_text()

                # Strip out any newline characters in the <td> cell and replace them with spaces
                value = str.join(' ', value.splitlines())
                entry[keys[index]] = value

            address_array.append(entry)
        return address_array

    @staticmethod
    def _filter_keys(list_of_dicts, keys_to_keep):
        """

        Given a list of keys and a list of dictionaries, this function will cycle through each dictionary in the list
        and strip out any keys that are not in the list

        :param list_of_dicts: the list of dictionaries to process
        :type list_of_dicts: list(dict)
        :param keys_to_keep: the keys in each dictionary you want to keep
        :type keys_to_keep: list(str)
        :return: the processed list of dicts
        :rtype: list(dict)
        """
        new_list_of_dicts = []
        for item in list_of_dicts:
            new_obj = {key: item[key] for key in keys_to_keep}
            new_list_of_dicts.append(new_obj)
        return new_list_of_dicts

    @staticmethod
    def _filter_by_ip(list_of_dicts):
        """

        Cycles through a list of dictionaries and drops any dictionary where the value of the 'ip' key doesn't
        match the ip address regex pattern

        :param list_of_dicts: the list of dictionaries to process
        :type list_of_dicts: list(dict)
        :return: the processed list of dicts
        :rtype: list(dict)
        """
        ip_addr_regex = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        new_list_of_dicts = []
        for item in list_of_dicts:
            # Remove whitespace at the end of our ip field to aid in matching
            item['IP Address'] = item['IP Address'].rstrip()
            # if the item we're looking at has a valid IP address, add it to the new list. otherwise skip it.'
            if re.match(ip_addr_regex, item['IP Address']):
                new_list_of_dicts.append(item)
        return new_list_of_dicts
