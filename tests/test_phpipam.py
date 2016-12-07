import re
import ConfigParser

from phpipam_scraper import IPAM
import pytest

@pytest.fixture()
def conf():
    conf_variables = ConfigParser.ConfigParser()
    conf_variables.read('variables.cfg')
    return conf_variables


def test_is_the_test_rig_setup(conf):
    message = 'You have not set up the testing variables file to run this test, or the testing variables file is ' \
              'missing options. Please run setup_tests.py first'
    assert conf.has_option('config', 'url'), message
    assert conf.has_option('phpipam', 'username'), message
    assert conf.has_option('phpipam', 'password'), message


@pytest.fixture()
def ipam(conf):
    username = conf.get('phpipam', 'username')
    password = conf.get('phpipam', 'password')
    url = conf.get('config', 'url')
    ipam = IPAM(username, password, url)
    return ipam


def test_ipam_search(ipam, conf):
    keyword = conf.get('test variables', 'search result')
    results = ipam.get_from_search(keyword)
    ip_addr_regex = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    assert type(results) is list
    assert len(results) is 1
    for item in results:
        assert type(item) is dict
        assert 'IP Address' in item.keys()
        assert 'Hostname' in item.keys()
        assert 'Description' in item.keys()
        assert re.match(ip_addr_regex, item['IP Address'])


def test_ipam_device(ipam, conf):
    keyword = conf.get('test variables', 'device result')
    results = ipam.get_from_devices(keyword)
    ip_addr_regex = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    assert type(results) is list
    assert len(results) is 1
    for item in results:
        assert type(item) is dict
        assert 'IP Address' in item.keys()
        assert 'Hostname' in item.keys()
        assert 'Description' in item.keys()
        assert re.match(ip_addr_regex, item['IP Address'])


def test_ipam_single_result(ipam, conf):
    keyword = conf.get('test variables', 'single result')
    results = ipam.get_all(keyword)
    ip_addr_regex = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    assert type(results) is list
    assert len(results) is 1
    for item in results:
        assert type(item) is dict
        assert 'IP Address' in item.keys()
        assert 'Hostname' in item.keys()
        assert 'Description' in item.keys()
        assert 'Source' in item.keys()
        assert re.match(ip_addr_regex, item['IP Address'])


def test_ipam_many_results(ipam, conf):
    keyword = conf.get('test variables', 'many results')
    results = ipam.get_all(keyword)
    ip_addr_regex = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    assert type(results) is list
    assert len(results) > 1
    for item in results:
        assert type(item) is dict
        assert 'IP Address' in item.keys()
        assert 'Hostname' in item.keys()
        assert 'Description' in item.keys()
        assert 'Source' in item.keys()
        assert re.match(ip_addr_regex, item['IP Address'])


def test_ipam_no_result(ipam, conf):
    keyword = conf.get('test variables', 'no result')
    results = ipam.get_all(keyword)
    assert type(results) is list
    assert len(results) is 0