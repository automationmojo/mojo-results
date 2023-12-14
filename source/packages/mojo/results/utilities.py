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

from typing import List

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

    directory_items = [item for item in os.listdir(rootdir)]
    directory_items.sort()

    dirnames = []
    filenames = []

    for dentry in directory_items:

        if dentry == "." or dentry == "..":
            continue

        dentry_full = os.path.join(rootdir, dentry)

        if os.path.isfile(dentry_full):
            filenames.append(dentry)
        elif os.path.isdir(dentry_full):
            if dentry not in dont_catalog_dirs:
                dirnames.append(dentry)
        
            if dentry not in dont_descend_dirs:
                if not os.path.islink(dentry_full):
                    catalog_tree(dentry_full, dont_catalog_dirs, dont_descend_dirs)

    # Don't write the catalog file untile we have walked a directory
    catalog = {
        "files": filenames,
        "folders": dirnames
    }

    catalogfile = os.path.join(rootdir, "catalog.json")

    with open(catalogfile, 'w') as cf:
        json.dump(catalog, cf, indent=4)

    return

