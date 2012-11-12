#!/usr/bin/env python

"""
	Integrates all the scripts of the given directory on the galaxy distance.
"""

__author__ = "Jose Antonio Navas"
__copyright__ = "Copyright 2011, The QIIME Project"
__credits__ = ["Jose Antonio Navas"]
__license__ = "GPL"
__version__ = "1.4.0-dev"
__maintainer__ = "Jose Antonio Navas"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from os import path, mkdir, walk, remove, environ
from site import addsitedir
from xml.dom.minidom import parse, Document
from xml_generator import make_xml
import commands

def parse_config_file(lines):
	"""
		lines: configuration file which contains the section structure of the scripts

		Returns:
			result: dict of {script:(section, remove_opts)}
			sections: list which contains all the different sections which tools are classified
	"""
	result = {}
	sections = []

	current_section = None

	for line in lines:
		if line and line != "\n":
			if line.startswith('#'):
				continue
			elif line.startswith('\t'):
				current_section = line.split('\t')[1].replace('\n', '')
				sections.append(current_section)
			else:
				if current_section is None:
					raise ValueError, 'Bad configuration file'
				fields = line.split()
				try:
					result[fields[0]] = (current_section, fields[1])
				except IndexError:
					result[fields[0]] = (current_section, None)

	return result, sections

def create_dirs(galaxy_dir, sections):
	"""
		galaxy_dir: galaxy home directory path
		sections: list which contains all the different sections which tools are classified

		Create the section's directories under the path galaxy_dir/tools, if they does not exists
	"""
	tools_dir = path.join(galaxy_dir, 'tools')

	if not path.exists(tools_dir):
		raise ValueError, 'Wrong galaxy installation path'

	for sect in sections:
		sect = sect.replace(" ", "").lower()
		dir_path = path.join(tools_dir, sect)
		if not path.exists(dir_path):
			mkdir(dir_path)

def get_galaxy_tool_conf_file(galaxy_dir, update):
	"""
		galaxy_dir: galaxy home directory path
		update: boolean to know if we had to update the tool_conf or generate a new one

		Returns a xml.dom.minidom.Document object which contains the tool_conf.xml file
	"""
	tool_conf_fp = path.join(galaxy_dir, 'tool_conf.xml')

	if not path.exists(tool_conf_fp):
		raise ValueError, 'Wrong galaxy installation path'

	if update:
		return parse(tool_conf_fp)
	else:
		tool_conf = Document()

		toolbox = tool_conf.createElement("toolbox")
		tool_conf.appendChild(toolbox)

		section = tool_conf.createElement("section")
		section.setAttribute("name", "Get Data")
		section.setAttribute("id", "getext")
		toolbox.appendChild(section)

		tool = tool_conf.createElement("tool")
		tool.setAttribute("file", "data_source/upload.xml")
		section.appendChild(tool)

		return tool_conf

def get_section_node(section, xml):
	"""
		section: section name which we are looking for
		xml: xml document where to find the section

		Return the section node if it exists, None otherwise
	"""
	for node in xml.getElementsByTagName('section'):
		if node.attributes.getNamedItem('name').value == section:
			return node
	return None

def exist_script_in_section(script, section_node):
	"""
		script: script which we are looking for
		section_node: xml node where to find the script

		Return True if the script already exists in this section_node, False otherwise
	"""
	name, ext = path.splitext(script)
	filepath = section_node.attributes.getNamedItem('name').value.replace(" ", "").lower() + "/" + name + ".xml"

	for node in section_node.childNodes:
		if node.attributes != None and node.attributes.getNamedItem('file').value == filepath:
			return True
	return False

def add_section_to_xml(section, script_list, xml):
	"""
		section: section to add to the xml
		script_list: list with the scripts to add under the section
		xml: xml object where to add the section
	"""
	toolbox = xml.firstChild

	section_node = xml.createElement('section')
	section_node.setAttribute("name", section)
	section_node.setAttribute("id", section.replace(" ", "").lower())
	toolbox.appendChild(section_node)

	for script in script_list:
		name, ext = path.splitext(script)
		filepath = section.replace(" ", "").lower() + "/" + name + ".xml"

		tool_node = xml.createElement('tool')
		tool_node.setAttribute("file", filepath)
		section_node.appendChild(tool_node)


def update_tool_conf_xml(tool_conf, section_dict):
	for section in section_dict.keys():
		section_node = get_section_node(section, tool_conf)
		if section_node:
			for script in section_dict[section]:
				if not exist_script_in_section(script, section_node):
					name, ext = path.splitext(script)
					filepath = section.replace(" ", "").lower() + "/" + name + ".xml"
					tool_node = tool_conf.createElement('tool')
					tool.setAttribute("file", filepath)
					section_node.appendChild(tool_node)
		else:
			add_section_to_xml(section, section_dict[section], tool_conf)

def integrate(scripts_dir, galaxy_dist_dir, config_file, update_tool_conf, log_fp):
	"""
		scripts_dir: full path to the directory which contains the scripts to integrate
		galaxy_dist_dir: full path to the Galaxy home directory
		config_file: path to the configuration file which contains the section structure of the scripts
	"""
	script_dict, sections = parse_config_file(open(config_file, 'U'))

	create_dirs(galaxy_dist_dir, sections)

	tool_conf = get_galaxy_tool_conf_file(galaxy_dist_dir, update_tool_conf)

	section_dict = {}
	for section in sections:
		section_dict[section] = []

	if not log_fp:
		log_fp = path.join(scripts_dir, 'integration.log')

	log_file = open(log_fp, 'w')

	addsitedir(scripts_dir)

	for root, dirs, files in walk(scripts_dir):
		for name in files:
			if name.endswith('.py'):
				log_file.write("Generating XML file for %s script... " % name)
				if name in script_dict.keys():
					section, remove_opts = script_dict[name]
					output_dir = path.join(galaxy_dist_dir, 'tools', section.replace(" ", "").lower())
					try:
						make_xml(name, output_dir, remove_opts)
						section_dict[section].append(name)
						log_file.write("Ok\n")
					except Exception as exc:
						log_file.write(str(type(exc)) + " : " + str(exc) + "\n")
				else:
					log_file.write("skipped - not in configuration file\n")


	log_file.write("Generating tool_conf... ")
	update_tool_conf_xml(tool_conf, section_dict)
	log_file.write("Ok\n")

	log_file.write("Writing tool_conf... ")
	# Write tool_conf.xml file
	tool_conf_fp = path.join(galaxy_dist_dir, 'tool_conf.xml')
	f = open(tool_conf_fp, 'w')
	f.write(tool_conf.toprettyxml(indent='\t'))
	f.close()
	log_file.write("Ok\n")

	log_file.write("Updating environment... ")
	command_string = 'echo "\nexport GALAXY_HOME=%s" >> ~/.bashrc' % path.abspath(galaxy_dist_dir)
	(append_status, append_out) = commands.getstatusoutput(command_string)
	if append_status != 0:
		raise ValueError, "Error updating environment"
	else:
		log_file.write("Ok\n")

	# Close log file
	log_file.close()