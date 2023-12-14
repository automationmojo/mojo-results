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

from typing import Dict, List

import os
import json

DEFAULT_DO_NOT_CATALOG_DIRS = [
    "__pycache__"
]

DEFAULT_DO_NOT_DESCEND_DIRS = [
    "diagnostics"
]

def catalog_tree(rootdir: str, dont_catalog_dirs: List[str] = DEFAULT_DO_NOT_CATALOG_DIRS,
                 dont_descend_dirs: List[str] = DEFAULT_DO_NOT_DESCEND_DIRS):
    """
        Adds json catalog files to a file system tree to help provide directory
        services to javascript in html files.
    """

    directory_items = [item for item in os.listdir()]

    dirnames = []
    filenames = []

    for ditem in directory_items:

        if ditem == "." or ditem == "..":
            continue

        if os.path.isfile(ditem):
            filenames.append(ditem)
        elif os.path.isdir(ditem):
            if ditem not in dont_catalog_dirs:
                dirnames.append(ditem)
        
            if ditem not in dont_descend_dirs:
                child_dir_full = os.path.join(rootdir, ditem)
                catalog_tree(child_dir_full, dont_catalog_dirs, dont_descend_dirs)

    # Don't write the catalog file untile we have walked a directory
    catalog = {
        "files": filenames,
        "folders": dirnames
    }

    catalogfile = os.path.join(rootdir, "catalog.json")

    with open(catalogfile, 'w') as cf:
        json.dump(catalog, cf, indent=4)

    return

