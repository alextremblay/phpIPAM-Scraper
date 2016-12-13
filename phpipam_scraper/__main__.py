"""

"""

__version__ = '1.1.2'

import click
from click_shell import shell
from tabulate import tabulate
from .phpipam import IPAM
from .config import set_url, get_url

ipam = None

@shell(prompt='phpipam>',
       intro="Welcome to the phpIPAM Scraper shell utility version " + __version__ + ". type a command to begin, type "
             "'?' or 'help' for a list of supported commands, or type 'quit' or 'exit' to quit",
       help="A command-line tool for retrieving device information (Description, Hostname, IP Address) from a "
            "phpIPAM installation")
@click.pass_context
@click.option('-u', '--username')
@click.option('-p', '--password')
def cli(ctx, username, password):
    global ipam
    if username or password:
        ipam = IPAM(username, password)


@cli.group(help='Commands to retrieve info from phpIPAM. Must be called with a subcommand.')
def get():
    pass


@cli.group(name='config', help="Commands for working with this tool's stored configuration. Must be called "
                               "with a subcommand.")
def conf():
    pass


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
def all(keyword):
    global ipam
    if ipam is None:
        ipam = IPAM()
    results = ipam.get_all(keyword)
    click.echo(tabulate(results, headers='keys'))


@conf.command(name='set-url', help="Specify a new phpIPAM URL for this tool to connect to from now on")
@click.argument('url')
def set_url(url):
    set_url(url)
    click.echo('New phpIPAM URL set!')


@conf.command(name='get-url', help="Show the currently configured phpIPAM URL to connect to.")
def get_url():
    click.echo(get_url())