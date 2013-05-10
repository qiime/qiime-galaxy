#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The Galaxy-QIIME Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

import tarfile
from shutil import move
from os import path

ERROR_MSG = "The input file is not a tar file!"

def compress_to_tgz(in_path, tgz_fp):
    """Generate a tgz file with the contents of the provided path

    Input:
        in_path: path to include in the tgz file
        tgz_fp: path to the result tgz file
    """
    t = tarfile.open(name = tgz_fp, mode = 'w:gz')
    t.add(in_path, path.basename(in_path))
    t.close()

def extract_from_tgz(tgz_file, output_path):
    """Extract the contents of the tgz file in the provided output path

    Input:
        tgz_file: filepath to the tgz file
        output_path: path to the output directory

    If the tgz_file only contains one file, it is extracted and renamed as the
    path indicated 'output_path'

    Note: raises a ValueError if tgz_file is not a tgz_file
        If there is any other error during the extraction, it propagates the
        error raised by tarfile
    """
    try:
        t = tarfile.open(name = tgz_file, mode = 'r')
    except tarfile.ReadError:
        raise ValueError, ERROR_MSG
    else:
        names_list = t.getnames()
        # if the tgz_file only has one file is not necessary to generate an
        # output directory
        if len(names_list) == 1:
            t.extractall()
            move(names_list[0], output_path)
        else:
            t.extractall(path=output_path)
        t.close()
    