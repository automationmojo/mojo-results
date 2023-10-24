"""
.. module:: utilities
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module with utilility functions for processing results.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"


import os
import json

def catalog_tree(rootdir: str, ignore_dirs=[]):
    """
        Adds json catalog files to a file system tree to help provide directory
        services to javascript in html files.
    """
    for dirpath, dirnames, filenames in os.walk(rootdir, topdown=True):
        dir_base_name = os.path.basename(dirpath)
        if dir_base_name not in ignore_dirs:

            for igdir in ignore_dirs:
                if igdir in dirnames:
                    dirnames.remove(igdir)

            catalog = {
                "files": filenames,
                "folders": dirnames
            }

            catalogfile = os.path.join(dirpath, "catalog.json")
            with open(catalogfile, 'w') as cf:
                json.dump(catalog, cf, indent=4)

    return
