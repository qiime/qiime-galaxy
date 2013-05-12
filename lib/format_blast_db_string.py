#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The Galaxy-QIIME Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from os.path import isdir, splitext, join
from os import listdir

def format_blast_db_string(in_path):
    """Generate a string with the path to the blast database

    Input:
        in_path: the path to the blast database base directory or to a fasta
            file with the reference sequences to create the DB on-the-fly
    """
    if isdir(in_path):
        # The path is the base directory of a blast database
        # Get one file of the directory
        f = listdir(in_path)[0]
        f = join(in_path, f)
        # Get the base path of the file
        basepath, ext = splitext(f)
        return basepath
    else:
        # The path is a fasta file
        return in_path