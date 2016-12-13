
Welcome to phpIPAM-Scraper's documentation!
*******************************************

Welcome to the API documentation.


phpipam module
==============

**class phpipam_scraper.phpipam.IPAM(username=None, password=None,
url=None)**

   The main class for this entire project. Stores all information
   related to a connection to a give phpIPAM installation. During
   initialization, it will prompt for username and password if one is
   not supplied, and will attempt to retrieve the URL for the phpIPAM
   installation from a config file if a URL is not specified. It will
   then attempt to login and open a persistent session to process
   future requests.

   :Parameters:
      * **username** (*str** or **None*) -- The username for your
        phpIPAM account

      * **password** (*str** or **None*) -- The password  for your
        phpIPAM account

      * **url** (*str** or **None*) -- The URL to connect to

   **get_all(keyword)**

      Calls self.get_from_search and self.get_from_device together,
      combines their results, tags each entry with a         source to
      denote where it came from

      :Parameters:
         **keyword** (*str*) -- keyword to search by

      :Returns:
         list of dicts containing hostname, IP, description, and
         source for each device found

      :Return type:
         list(dict)

   **get_from_devices(keyword)**

      Retrieves device information from phpIPAM's devices page

      :Parameters:
         **keyword** (*str*) -- keyword to search by

      :Returns:
         list of dicts containing hostname, IP, and description for
         each device found

      :Return type:
         list(dict)

   **get_from_search(keyword)**

      Retrieves device information from phpIPAM's search page

      :Parameters:
         **keyword** (*str*) -- keyword to search by

      :Returns:
         list of dicts containing hostname, IP, and description for
         each device found

      :Return type:
         list(dict)


config module
=============

**phpipam_scraper.config.first_time_setup()**

   If an attempt is make to retireve the phpIPAM URL from store config
   file, but no stored config file exists, this function is called to
   prompt the user for a URL to store, and sets the URL received from
   the user

**phpipam_scraper.config.get_url()**

   Retrieves stored URL from a configuration file stored in one of 3
   locations on the system. See the paths variable in
   phpipam_scraper.config for details on where this file is stored

   :Returns:
      URL of the phpIPAM site to connect to

   :Return type:
      str or Exception

**phpipam_scraper.config.set_url(url)**

   Set URL for phpIPAM site to connect to, and store variable in a
   onfiguration file stored in one of 3 locations on the system. See
   the paths variable in phpipam_scraper.config for details on where
   this file is stored

   :Parameters:
      **url** (*str*) -- URL of the phpIPAM site to connect to

   :Returns:
      True on success, Exception on failure

   :Return type:
      bool or Exception


Indices and tables
******************

* `Index <genindex>`_

* `Module Index <py-modindex>`_

* `Search Page <search>`_
