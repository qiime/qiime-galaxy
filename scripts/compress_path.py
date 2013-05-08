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
from tgz_manager import compress_to_tgz

script_info = {}
script_info['brief_description'] = """Generate a tgz file with the contents of\
 the provided path compressed"""
script_info['script_description'] = """If input_path is a file: generate a tgz\
 file with the input file compressed.
If input_path is a directory: generate a tgz file with the content of the input\
 directory compressed."""
script_info['script_usage'] = [("Example:",
"Generate a tgz file named 'out.tgz' which contains the content of the\
 directory 'in_dir'",
"%prog -i in_dir -o out.tgz")]
script_info['output_description'] = "A tgz file"
script_info['required_options'] = [
    make_option('-i', '--input_path', type="existing_path",
                help='Path to the directory or file to compress'),
    make_option('-o', '--output_tgz', type="new_filepath",
                help='File path of the output tgz file')
]
script_info['optional_options'] = []
script_info['version'] = __version__

if __name__ == '__main__':
    option_parser, opts, args = parse_command_line_parameters(**script_info)
    input_path = opts.input_path
    tgz_fp = opts.output_tgz

    compress_to_tgz(input_path, tgz_fp)