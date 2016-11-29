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
import config


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        ctx.ipam = IPAM()
        ctx.invoke(repl)
    elif ctx.invoked_subcommand is not 'set-url':
        ctx.ipam = IPAM()


@cli.command(name='set-url')
@click.option('-u', '--url', prompt='Please specify a new URL to set in the phpIPAM config file')
def set_url(url):
    config.set_url(url)
    click.echo('New phpIPAM URL set!')


@cli.command()
@click.pass_context
@click.option('-d', '--deep', is_flag=True)
@click.argument('keyword')
def get(ctx, keyword, deep):
    results = ctx.ipam.get(keyword)
    click.echo(tabulate(results, headers=['Hostname', 'IP Address']))


@cli.command()
@click.pass_context
def repl(ctx):
    click_repl.repl(ctx)
