#!/usr/bin/env python

"""Integrates all the scripts of the given directory on the galaxy distance."""

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2011, The QIIME Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "1.4.0-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from cogent.util.option_parsing import parse_command_line_parameters, make_option
from galaxy_integration import integrate

script_info = {}
script_info['brief_description'] = "Integrate the scripts from the given directory on the given Galaxy instance"
script_info['script_description'] = "For each script in 'input_dir', generates the XML file, puts the XML file in the right Galaxy directory and updates the Galaxy's tool_conf.xml file."
script_info['script_usage'] = [("Example:", "Integrate the scripts under 'scripts_dir' on the Galaxy instante 'galaxy_dist_dir' using the configuration file 'config_file.txt'", "%prog -i scripts_dir -g galaxy_dist_dir -c config_file.txt")]
script_info['output_description'] = ""
script_info['required_options'] = [
	make_option('-i', '--input_dir', type="existing_dirpath",
				help='directory which contains the scripts to integrate'),
	make_option('-g', '--galaxy_dist_dir', type="existing_dirpath",
				help='Galaxy home directory'),
	make_option('-c', '--config_file', type="existing_filepath",
				help='Configure file which contains the section structure of the scripts')
]
script_info['optional_options'] = [
	make_option('--update_tool_conf', action='store_true',
				help='By default, the Galaxy tool_conf file is overwritten. Use this option to not overwrite it and update it.'),
	make_option('-l', '--log_file', type='new_filepath',
				help='File path where to store the log file. [Default: input_dir/integration.log]')
]
script_info['version'] = __version__

if __name__ == '__main__':
	option_parser, opts, args = parse_command_line_parameters(**script_info)
	input_dir = opts.input_dir
	galaxy_dir = opts.galaxy_dist_dir
	config_file_fp = opts.config_file
	update = opts.update_tool_conf
	log_fp = opts.log_file

	integrate(input_dir, galaxy_dir, config_file_fp, update, log_fp)