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
import sys

import click
from click_shell import shell
from tabulate import tabulate
from .phpipam import IPAM
import config

ipam = None

@shell(prompt='phpipam>', intro='Welcome to the phpIPAM Scraper shell utility. type a command to begin')
@click.pass_context
@click.option('-u', '--username')
@click.option('-p', '--password')
def cli(ctx, username, password):
    global ipam
    if username or password:
        ipam = IPAM(username, password)


@cli.command(name='set-url')
@click.argument('url')
def set_url(url):
    config.set_url(url)
    click.echo('New phpIPAM URL set!')


@cli.command(name='get-url')
def get_url():
    click.echo(config.get_url())


@cli.command()
@click.option('-d', '--deep', is_flag=True)
@click.argument('keyword')
def get(deep, keyword):
    global ipam
    if ipam is None:
        ipam = IPAM()
    results = ipam.get_from_devices(keyword)
    if deep:
        results += ipam.get_from_search(keyword)
        
    click.echo(tabulate(results, headers=['Hostname', 'IP Address']))
