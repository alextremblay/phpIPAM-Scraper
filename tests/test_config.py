import re


from phpipam_scraper import config
import pytest


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