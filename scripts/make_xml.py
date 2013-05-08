#!/usr/bin/env python

"""Generate a xml file for Galaxy from a qiime python script"""

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2011, The QIIME Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "1.4.0-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from cogent.util.option_parsing import parse_command_line_parameters, make_option
from xml_generator import make_xml

script_info = {}
script_info['brief_description'] = "Generates a Galaxy XML file from a given QIIME script"
script_info['script_description'] = "Reads the input script, looks for his 'script_info' and extract all the information necessary to generate the XML file. The script generated takes the same name as the original script, but changing his extension to XML. Once the XML is generated, the script must be put into the Galaxy's tools folder and edit tool_conf.xml "
script_info['script_usage'] = [("Example:", "Generate the Galaxy XML file from the script 'my_script.py' without including the '--opt_a' and the '--opt_b' options.", "%prog -i my_script.py -r opt_a,opt_b")]
script_info['output_description'] = "An XML file that Galaxy can reads and make the tool available via web browser"
script_info['required_options'] = [
	make_option('-i', '--script_fp', type="existing_filepath",
				help='the QIIME python script filepath to generate'),
	make_option('-o', '--output_dir', type="existing_dirpath",
				help='output directory where to save the XML file')
]
script_info['optional_options'] = [
	make_option('-r', '--remove_opts', type="string",
				help='List of option names (e.g. "option1,option2") that will not appear in the xml'),
]
script_info['version'] = __version__

if __name__ == '__main__':
	option_parser, opts, args = parse_command_line_parameters(**script_info)
	script_fp = opts.script_fp
	output_dir = opts.output_dir
	remove_opts = opts.remove_opts

	make_xml(script_fp, output_dir, remove_opts)