from mock import Mock
import sys
import os

from phpipam_scraper import config


check = config.check = Mock()
read = config.read = Mock()
write = config.write = Mock()
get_input = config.get_input = Mock()
log = config.log = Mock()

if sys.platform == 'win32':
    sys_path = os.path.join(os.getenv('LOCALAPPDATA'), 'phpipam', 'phpipam.cfg')
    user_path = os.path.join(os.getenv('USERPROFILE'), 'phpipam', 'phpipam.cfg')
else:
    sys_path = os.path.join('/', 'usr', 'local', 'phpipam', 'phpipam.cfg')
    user_path = os.path.expanduser('~/.local/phpipam/phpipam.cfg')


def test_get_url_no_file():
    check.return_value = False
    get_input.return_value = 'http://someurl.com'
    read.return_value = 'http://someurl.com'

    try:
        assert config.get_url_from_config_file() == 'http://someurl.com'
    except Exception as e:
        assert len(e.message) > 0

    assert check.call_count == 2
    assert get_input.called
    assert get_input.call_count == 2
    assert write.called
    assert log.called


def test_get_url_file_exists():
    check.return_value = True
    read.return_value = 'http://someurl.com'

    assert config.get_url_from_config_file() == 'http://someurl.com'

    assert check.called
    print(get_input.call_args)
    print get_input.assert_not_called()
    print write.assert_not_called()
    print log.assert_not_called()

def test_get_url_no_write_perm():
    pass