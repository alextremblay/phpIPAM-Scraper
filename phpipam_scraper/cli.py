"""

"""

__version__ = '1.1.2'

import click
from click_shell import shell
from tabulate import tabulate
from .main import IPAM, get_config, delete_config
from .log import getLogger, enable_console_logging, enable_file_logging

ipam = None

@shell(prompt='phpipam>',
       intro="Welcome to the phpIPAM Scraper shell utility version " + __version__ + ". type a command to begin, type "
             "'?' or 'help' for a list of supported commands, or type 'quit' or 'exit' to quit",
       help="A command-line tool for retrieving device information (Description, Hostname, IP Address) from a "
            "phpIPAM installation")
@click.pass_context
@click.option('-u', '--username')
@click.option('-p', '--password')
@click.option('-v', '--verbose', count=True)
def main(ctx, username, password, verbose):
    if verbose > 0 and verbose < 5:
        enable_console_logging(verbose)
    if verbose >= 5:
        enable_console_logging(4)
        enable_file_logging('/tmp/phpipam.log')
    log = getLogger('cli')
    ctx.obj = {
        'username': username,
        'password': password
    }
    log.debug_obj('ctx:', ctx)


@main.group(help='Commands to retrieve info from phpIPAM. Must be called with a subcommand.')
@click.pass_context
def get(ctx):
    global ipam
    ipam = IPAM(ctx.obj['username'], ctx.obj['password'])


@get.command(help="Search the 'IP Addresses' section of phpIPAM's search page for a given keyword")
@click.argument('keyword')
def search(keyword):
    global ipam
    if ipam is None:
        ipam = IPAM()
    results = ipam.get_from_search(keyword)
    click.echo(tabulate(results, headers='keys'))


@get.command(help="Search phpIPAM's Devices page for a given keyword")
@click.argument('keyword')
def device(keyword):
    global ipam
    if ipam is None:
        ipam = IPAM()
    results = ipam.get_from_devices(keyword)
    click.echo(tabulate(results, headers='keys'))


@get.command(help="Search all available sources in phpIPAM for a given keyword")
@click.argument('keyword')
def combined(keyword):
    global ipam
    if ipam is None:
        ipam = IPAM()
    results = ipam.get_all(keyword)
    click.echo(tabulate(results, headers='keys'))


@main.group(name='config',
            help="Commands for working with this tool's stored configuration. "
                "Must be called with a subcommand.")
def conf():
    pass


@conf.command(name='set',
              help="(re)runs the configuration setup script to generate a new "
                   "config file")
def run_setup():
    delete_config()
    get_config()


@conf.command(name='get',
              help="Show the currently configured phpIPAM settings.")
def get_info():
    config = get_config()
    if config.get('url'):
        click.echo("URL: " + config['url'])
    else:
        click.echo("URL not configured")
    if config.get('username'):
        click.echo("Username: " + config['username'])
    else:
        click.echo("Username not configured")
    if config.get('password'):
        click.echo("Password is configured")
    else:
        click.echo("Password is not configured")
