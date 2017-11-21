What Is This?
=============

This folder contains all files necessary to run a pre-configured phpIPAM test environment in a set of docker containers.
Running `docker-compose up -d` in this directory will launch a mysql database prepopulated with phpIPAM sections, vlans, IP addresses, and devices, and will launch an apache container running phpIPAM

Account Details
===============

In case you ever need to make changes to the test environment, or just want to play around with it, here are the account username/passwords you may need:
MySQL:
    root/my-secret-pw
phpIPAM:
    admin/phpipamadminpw
    operator/operatorpw
    guestuser/guestpass
    normaluser/normaluserpw