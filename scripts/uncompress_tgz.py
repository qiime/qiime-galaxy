#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The Galaxy-QIIME Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from cogent.util.option_parsing import (parse_command_line_parameters, 
                                        make_option)
from shutil import copyfile
from tgz_manager import extract_from_tgz, ERROR_MSG

script_info = {}
script_info['brief_description'] = "Extract the content of a tgz file."
script_info['script_description'] = """If input_tgz has one file: extracts it\
 and renames it as output_path.
If input_tgz has multiple files: extracts them in a directory named output_path.
If input_tgz is not a tgz file (must be a file, not a directory): renames\
 the input file as output_path"""
script_info['script_usage'] = [("Example:",
"Extract the content of the tgz file named 'in.tgz' into the\
 directory 'out_dir'",
"%prog -i in.tgz -o out_dir")]
script_info['output_description'] = """A folder with the contents of the tgz\
 file or a single file if the tgz file only contains one file or the input file\
 is a single file and it is not a tgz file"""
script_info['required_options'] = [
    make_option('-i', '--input_tgz', type="existing_filepath",
                help='File path for the tgz file to uncompress'),
    make_option('-o', '--output_path', type="new_path",
                help='Path where to extract the contents of the tgz file')
]
script_info['optional_options'] = []
script_info['version'] = __version__

def extract_if_is_tgz(tgz_fp, output_path):
    """Extracts the contents of tgz_fp if it is a tgz file

    Inputs:
        tgz_fp: path to the tgz file
        output_path: path to the output directory or file

    If tgz_fp is not a tgz file, copies it to output_path

    Note: propagates the errors from 'extract_from_tgz'
    """
    try:
        extract_from_tgz(tgz_fp, output_path)
    except ValueError, e:
        # The input tgz_fp was a single file, copy it as 'output_path'
        if str(e) == ERROR_MSG:
            copyfile(tgz_fp, output_path)
        else:
            raise ValueError, e

if __name__ == '__main__':
    option_parser, opts, args = parse_command_line_parameters(**script_info)
    tgz_fp = opts.input_tgz
    output_path = opts.output_path

    extract_if_is_tgz(tgz_fp, output_path)