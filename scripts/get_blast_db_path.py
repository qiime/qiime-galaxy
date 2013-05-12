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
from format_blast_db_string import format_blast_db_string

script_info = {}
script_info['brief_description'] = "Prints to standard output the path to a \
blast database"
script_info['script_description'] = """This script takes a path and it\
 determines if the path is the base directory of blast database or it is a\
 fasta file with the reference sequences needed to create a blast database\
 on-the-fly"""
script_info['script_usage'] = [("Example:",
"Extract the content of the tgz file named 'in.tgz' into the\
 directory 'out_dir'",
"%prog -i in.tgz -o out_dir")]
script_info['output_description'] = """Prints through standard output the base\
 path of the blast database or the path to the reference sequence file,\
 depending on the input path"""
script_info['required_options'] = [
    make_option('-i', '--input_path', type="existing_path",
                help='Path to check')
]
script_info['optional_options'] = []
script_info['version'] = __version__

if __name__ == '__main__':
    option_parser, opts, args = parse_command_line_parameters(**script_info)
    in_path = opts.input_path

    path = format_blast_db_string(in_path)
    print path