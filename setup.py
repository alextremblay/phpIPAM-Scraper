from setuptools import find_packages, setup
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='phpIPAM-Scraper',
    version='1.1.4-incomplete',
    description='A python library to retrieve device IPs from a PHPipam installation',
    long_description=long_description,
    url='https://github.com/alextremblay/phpipam_scraper',
    author='Alex Tremblay',
    license='LGPLv3',
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Environment :: Console',

        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',

        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',

        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',

        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    packages=find_packages(),
    install_requires=[
        'configparser ; python_version < "3.2"',
        'requests',
        'beautifulsoup4',
        'tabulate',
        'click',
        'click-shell'],
    extras_require={
        'test': [
            'pytest',
            'pytest-docker',
            'pytest-docker-pexpect',
        ]
    },
    entry_points={
        'console_scripts': [
            'phpipam = phpipam_scraper.__main__:cli'
        ]
    }
)
