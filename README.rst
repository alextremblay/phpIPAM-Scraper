===============
phpIPAM-Scraper
===============

What is this?
-------------
This is a tool written in python to retrieve information on devices in phpIPAM based on a keyword supplied.

This package provides a python module to retrieve info, and a command-line tool for interactive information retrieval

The tool will grab and display a switch's IP address, hostname, and description


Module
------

*To Install:*
``pip install phpIPAM-Scraper``

*To Use:*
``import phpipam_scraper`` or ``from phpipam_scraper import IPAM``
The IPAM class accepts optional parameters for username, password, and URL. If these values are not supplied when
instantiating the class, this module will attempt to prompt for them from stdin.
see the `API Doc <https://github.com/alextremblay/phpIPAM-Scraper/blob/master/docs/apidoc.rst>`_ for additional information.


Command Line Tool
-----------------
the command line tool is called ``phpipam``  and can be used in one of two ways:

When called with an argument, it processes that specific request, and then exits. When called without a command, it
drops you into a shell from which you can run multiple subcommands.

The benefit of running the shell is that phpIPAM authentication details will only be asked for once, and will be stored
in memory until you exit the shell.

**Warning:** Please take caution when using the shell. Since phpIPAM username and password details are stored in memory
for as long as the shell is active, any *\*disreputable\** program running on your computer while the shell is running
**may** be able to access those details while the shell is running. Most operating systems prevent this sort of
behaviour, but not all do, so take care.

There are two main groups of commands which can be run from this command line tool: config and get.
**config** commands allow you to get or set the URL of the phpIPAM installation to connect to
**get** commands allow you to retrieve device information from phpIPAM's search page, device page, or both.
you can type ``phpipam [group] --help`` to get more information, or type ``help`` or ``?`` from within the shell to get
more information.

Want to contribute?
-------------------
See the see the project page / wiki on github for details