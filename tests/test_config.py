import re
import configparser

from phpipam_scraper import config
import pytest

@pytest.fixture()
def conf():
    conf_variables = configparser.ConfigParser()
    conf_variables.read('variables.cfg')
    conf_variables.read('tests/variables.cfg')
    return conf_variables


def test_is_the_test_rig_setup(conf):
    assert conf.has_option('config', 'url'), 'You have not set up the testing variables file to run ' \
                                                             'this test. Please run setup_tests.py first'


def test_get_url():
    url = config.get_url()
    assert type(url) is str
    assert re.match(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)', url)


def test_set_url():
    old_url = config.get_url()
    new_url = 'http://test.com'
    with pytest.raises(Exception):
        config.set_url(new_url)
    assert config.set_url(old_url)
    assert config.get_url() in old_url


def test_set_url_failure(conf):
    invalid_url = 'somerandomhostname'
    with pytest.raises(Exception):
        config.set_url(invalid_url)
        config.set_url(conf.get('config', 'url'))