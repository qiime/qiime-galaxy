#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2011, The QIIME Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "1.4.0-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from cogent.util.option_parsing import parse_command_line_parameters, make_option
from shutil import copyfile
from tgz_manager import extract_from_tgz, ERROR_MSG

script_info = {}
script_info['brief_description'] = "Extract the content of a tgz file."
script_info['script_description'] = """If input_tgz has one file: extract it an rename it as output_path.
If input_tgz has multiple files: extract them in a directory named output_path.
If input_tgz is not a tgz file (must be a file, not a directory): rename the input file as output_path"""
script_info['script_usage'] = [("Example:", "Extract the content of the tgz file named 'in.tgz' into the directory 'out_dir'", "%prog -i in.tgz -o out_dir")]
script_info['output_description'] = ""
script_info['required_options'] = [
	make_option('-i', '--input_tgz', type="existing_filepath",
				help='File path for the tgz file to uncompress'),
	make_option('-o', '--output_path', type="new_path",
				help='Path where to extract the contents of the tgz file')
]
script_info['optional_options'] = []
script_info['version'] = __version__

def extract_if_is_tgz(tgz_fp, output_path):
	try:
		extract_from_tgz(tgz_fp, output_path)
	except ValueError, e:
		# The input
		if str(e) == ERROR_MSG:
			copyfile(tgz_fp, output_path)
		else:
			raise ValueError, e


if __name__ == '__main__':
	option_parser, opts, args = parse_command_line_parameters(**script_info)
	tgz_fp = opts.input_tgz
	output_path = opts.output_path

	extract_if_is_tgz(tgz_fp, output_path)