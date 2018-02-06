import re


from phpipam_scraper import config
import os
import pytest

config_files = os.path.join(os.getcwd(), 'config_files')

@pytest.yield_fixture()
def test_paths():
    paths = {
        'config_file_absent': os.path.join(config_files, 'config_file_absent'),
        'system_file': os.path.join(config_files, 'no_file_exists',
                                    'system_dir', 'config')
    }
    # Ensure that the files specified in paths don't currently exist
    try:
        os.remove(paths['config_file_absent'] + '/testapplication')
    except FileNotFoundError:
        pass

    # Yield to the test function & begin test
    yield paths

    # Remove path files once test is complete
    for path in paths.values():
        try:
            os.remove(path)
        except FileNotFoundError:
            pass

def test_no_config_file_exists(monkeypatch, no_file_exists):
    '''
    
    Tests the config module's behaviour when no config file is found. It 
    should prompt for input, generate and save a new config file, load config 
    data from that file, and make that config data available in module 
    variables.

    '''

    def input_handler(prompt):
        if 'URL' in prompt:
            return 'http://localhost'
        if 'Username' in prompt:
            return 'TestUser'
        if 'Password' in prompt:
            return 'TestPassword'
        if '(yes/no)' in prompt:
            return 'y'
        else:
            assert False

    monkeypatch.setattr(config, 'get__user_input', input_handler)

    config.USER_FILE = no_file_exists['user_file']
    config.SYSTEM_FILE = no_file_exists['system_file']
    config.load_config()

    monkeypatch.undo()

    assert os.path.exists(config.USER_FILE)
    with open(config.USER_FILE) as f:
        line_count = sum(1 for line in f)
        assert line_count == 5

    assert config.url == 'http://localhost'
    assert config.username == 'TestUser'
    assert config.password == 'TestPassword'


def test_user_file_unwriteable(monkeypatch):
    '''
    
    Tests the config module's behaviour when no config file is found. It 
    should prompt for input, generate and save a new config file, load config 
    data from that file, and make that config data available in module 
    variables.

    '''

    def input_handler(prompt):
        if 'URL' in prompt:
            return 'http://localhost'
        if 'Username' in prompt:
            return 'TestUser'
        if 'Password' in prompt:
            return 'TestPassword'
        if 'Proceed' in prompt:
            return 'y'
        else:
            assert False

    monkeypatch.setattr(config, '_get_input', input_handler)
    monkeypatch.setattr(config, '_get_pass', input_handler)

    config.USER_FILE = os.path.join(config_files, 'user_file_unwritable',
                                    'user_dir', 'config')
    config.SYSTEM_FILE = os.path.join(config_files, 'user_file_unwritable',
                                      'system_dir', 'config')
    with pytest.raises(SystemExit):
        config.load_config()

    monkeypatch.undo()


def test_system_file_exists():
    '''
    
    Tests the config module's behaviour when only a system config file is 
    present. It should load config data from that file and make it available 
    in module variables

    '''

    config.USER_FILE = os.path.join(config_files, 'system_file_exists',
                                    'user_dir', 'config')
    config.SYSTEM_FILE = os.path.join(config_files, 'system_file_exists',
                                      'system_dir', 'config')
    config.load_config()

    assert config.url == 'http://localhost'
    assert config.username == 'TestUser'
    assert config.password == 'TestPassword'


def test_user_file_exists():
    '''

    Tests the config module's behaviour when only a user config file is 
    present. It should load config data from that file and make it available 
    in module variables

    '''

    config.USER_FILE = os.path.join(config_files, 'user_file_exists',
                                    'user_dir', 'config')
    config.SYSTEM_FILE = os.path.join(config_files, 'user_file_exists',
                                      'system_dir', 'config')
    config.load_config()

    assert config.url == 'http://localhost'
    assert config.username == 'TestUser'
    assert config.password == 'TestPassword'


def test_both_files_exist():
    '''

    Tests the config module's behaviour when a system config file and a user 
    config file are both present, and the user config file contains modified 
    versions of some information found in the system config file. It should 
    load config data from each file and override information from the system 
    file with matching information from the user config file before making it 
    available in module variables

    '''

    config.USER_FILE = os.path.join(config_files, 'both_files_exist',
                                    'user_dir', 'config')
    config.SYSTEM_FILE = os.path.join(config_files,
                                      'both_files_exist',
                                      'system_dir', 'config')
    config.load_config()

    assert config.url == 'http://localhost'
    assert config.username == 'OverriddenUser'
    assert config.password == 'OverriddenPassword'


def test_both_files_exist_exclusive():
    '''

    Tests the config module's behaviour when a system config file and a user 
    config file are both present, but each contains information that the 
    other does not. It should load config data from each file and make it 
    available in module variables

    '''

    config.USER_FILE = os.path.join(config_files, 'both_files_exist_exclusive',
                                    'user_dir', 'config')
    config.SYSTEM_FILE = os.path.join(config_files, 'both_files_exist_exclusive',
                                      'system_dir', 'config')
    config.load_config()

    assert config.url == 'http://localhost'
    assert config.username == 'TestUser'
    assert config.password == 'TestPassword'
