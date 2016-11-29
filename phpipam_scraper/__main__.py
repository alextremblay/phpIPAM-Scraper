"""
    phpipam
    USAGE: phpipam [OPTIONS] KEYWORD

    DESCRIPTION: This script shows a list of all devices on phpIPAM whose hostname matches the supplied keyword

    ARGUMENTS:
        KEYWORD              The IP Address of the switch you'd like to connect to.
    OPTIONS:
        -r                      Reset phpIPAM configuration file
        -h, --help              Show this help message and quit.

    SYNOPSIS:
        This script, when run, will connect to your configured phpIPAM installation and poll the devices list for
        any device whose hostname matches the keyword provided.
"""
import click
import click_repl
from tabulate import tabulate
from .phpipam import IPAM
from .config import set_url


@click.group()
@click.pass_context
def cli(ctx):
    ctx.forward(repl)

@click.command()
@click.argument('keyword')
def get(keyword):
    ipam = IPAM()
    results = ipam.get(keyword)
    click.echo(tabulate(results, headers=['Hostname', 'IP Address']))

@click.command()
@click.option('-u', '--url', prompt=True)
def reseturl(url):
    set_url(url)
    click.echo('New phpIPAM URL set!')

click_repl.register_repl('cli')
