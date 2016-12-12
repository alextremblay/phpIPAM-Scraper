import re
import configparser

from phpipam_scraper.__main__ import cli
from click.testing import CliRunner
import pytest

@pytest.fixture()
def conf():
    conf_variables = configparser.ConfigParser()
    conf_variables.read('variables.cfg')
    conf_variables.read('tests/variables.cfg')
    return conf_variables


def test_is_the_test_rig_setup(conf):
    message = 'You have not set up the testing variables file to run this test, or the testing variables file is ' \
              'missing options. Please run setup_tests.py first'
    assert conf.has_option('config', 'url'), message
    assert conf.has_option('phpipam', 'username'), message
    assert conf.has_option('phpipam', 'password'), message


@pytest.fixture()
def runner():
    cli_runner = CliRunner()
    return cli_runner


def test_help_base(runner):
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code is 0
    assert 'Usage' in result.output
    assert 'phpIPAM' in result.output


def test_help_get(runner):
    result = runner.invoke(cli, ['get', '--help'])
    assert result.exit_code is 0
    assert 'Usage' in result.output
    assert 'Commands' in result.output


def test_help_get_search(runner):
    result = runner.invoke(cli, ['get', 'search', '--help'])
    assert result.exit_code is 0
    assert 'Usage' in result.output
    assert "Search the 'IP Addresses' section" in result.output


def test_help_get_device(runner):
    result = runner.invoke(cli, ['get', 'device', '--help'])
    assert result.exit_code is 0
    assert 'Usage' in result.output
    assert "Search phpIPAM's Devices page" in result.output


def test_help_get_all(runner):
    result = runner.invoke(cli, ['get', 'all', '--help'])
    assert result.exit_code is 0
    assert 'Usage' in result.output
    assert 'Search all' in result.output


def test_help_config(runner):
    result = runner.invoke(cli, ['config', '--help'])
    assert result.exit_code is 0
    assert 'Usage' in result.output
    assert 'Commands' in result.output


def test_help_config_set(runner):
    result = runner.invoke(cli, ['config', 'set-url', '--help'])
    assert result.exit_code is 0
    assert 'Usage' in result.output
    assert 'Specify a new phpIPAM URL' in result.output


def test_help_config_get(runner):
    result = runner.invoke(cli, ['config', 'get-url', '--help'])
    assert result.exit_code is 0
    assert 'Usage' in result.output
    assert 'currently configured phpIPAM URL' in result.output


def test_config_get(runner):
    result = runner.invoke(cli, ['config', 'get-url'])
    url_regex = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'
    assert result.exit_code is 0
    assert re.match(url_regex, result.output)


def test_config_set(runner, conf):
    url = conf.get('config', 'url')
    result = runner.invoke(cli, ['config', 'set-url', url])
    assert result.exit_code is 0
    assert 'New phpIPAM URL set!' in result.output