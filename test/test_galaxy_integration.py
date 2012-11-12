#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2011, The QIIME Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "1.4.0-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from cogent.util.unit_test import TestCase, main
from os import path, mkdir, remove
from shutil import rmtree, copyfile
import tempfile
from xml.dom.minidom import Document
from galaxy_integration import (parse_config_file, create_dirs, get_galaxy_tool_conf_file, get_section_node,
									exist_script_in_section, add_section_to_xml, update_tool_conf_xml, integrate)

class GalaxyIntegrationTest(TestCase):
	def setUp(self):
		self.config_lines = config_lines.splitlines()
		self.bad_config_lines = bad_config_lines.splitlines()
		self.tmp_dir = tempfile.gettempdir()
		self.sections = ['Section1', 'Section2']

		self.script1 = './support_files/script1.py'
		self.script2 = './support_files/script2.py'
		self.script3 = './support_files/script3.py'
		self.config_file = './support_files/config_file.txt'

		self._paths_to_clean_up = []
		self._dirs_to_clean_up = []

	def tearDown(self):
		map(rmtree, self._dirs_to_clean_up)
		map(remove, self._paths_to_clean_up)

	def test_parse_config_file(self):
		obs_dict, obs_sections = parse_config_file(self.config_lines)
		exp_dict = {'script1.py':('Section 1', None),
			'script2.py':('Section 1', 'option1,option2'),
			'script3.py':('Section 2', None)}
		exp_sections = ['Section 1', 'Section 2']

		self.assertEqual(obs_dict, exp_dict)
		self.assertEqual(obs_sections, exp_sections)

		self.assertRaises(ValueError, parse_config_file, self.bad_config_lines)

	def test_create_dirs(self):
		galaxy_dir = tempfile.mkdtemp(dir=self.tmp_dir)
		self._dirs_to_clean_up = [galaxy_dir]
		galaxy_tools_dir = path.join(galaxy_dir, 'tools')
		mkdir(galaxy_tools_dir)
		create_dirs(galaxy_dir, self.sections)
		self.assertTrue(path.exists(path.join(galaxy_tools_dir, 'section1')),'The section directory was not created in the appropiate location')
		self.assertTrue(path.exists(path.join(galaxy_tools_dir, 'section2')),'The section directory was not created in the appropiate location')

		galaxy_dir = tempfile.mkdtemp(dir=self.tmp_dir)
		self._dirs_to_clean_up.append(galaxy_dir)
		self.assertRaises(ValueError, create_dirs, galaxy_dir, self.sections)

		galaxy_dir = tempfile.mkdtemp(dir=self.tmp_dir)
		self._dirs_to_clean_up.append(galaxy_dir)
		galaxy_tools_dir = path.join(galaxy_dir, 'tools')
		mkdir(galaxy_tools_dir)
		mkdir(path.join(galaxy_tools_dir, 'Section1'))
		create_dirs(galaxy_dir, self.sections)
		self.assertTrue(path.exists(path.join(galaxy_tools_dir, 'section1')),'The section directory was not created in the appropiate location')
		self.assertTrue(path.exists(path.join(galaxy_tools_dir, 'section2')),'The section directory was not created in the appropiate location')

	def test_get_galaxy_tool_conf_file(self):
		galaxy_dir = tempfile.mkdtemp(dir=self.tmp_dir)
		self._dirs_to_clean_up = [galaxy_dir]
		galaxy_tool_conf_fp = path.join(galaxy_dir, 'tool_conf.xml')
		f = open(galaxy_tool_conf_fp, 'w')
		f.write(existing_tool_conf_lines)
		f.close()
		obs_doc = get_galaxy_tool_conf_file(galaxy_dir, False)
		self.assertEqual(obs_doc.toprettyxml(indent="\t"), exp_doc_new)

		galaxy_dir = tempfile.mkdtemp(dir=self.tmp_dir)
		self._dirs_to_clean_up.append(galaxy_dir)
		galaxy_tool_conf_fp = path.join(galaxy_dir, 'tool_conf.xml')
		f = open(galaxy_tool_conf_fp, 'w')
		f.write(existing_tool_conf_lines)
		f.close()
		obs_doc = get_galaxy_tool_conf_file(galaxy_dir, True)
		self.assertEqual(obs_doc.toprettyxml(indent="\t"), exp_doc_existing)

		galaxy_dir = tempfile.mkdtemp(dir=self.tmp_dir)
		self._dirs_to_clean_up.append(galaxy_dir)
		self.assertRaises(ValueError, get_galaxy_tool_conf_file, galaxy_dir, False)

	def test_get_section_node(self):
		xml = Document()
		toolbox = xml.createElement('toolbox')
		xml.appendChild(toolbox)
		s1_node = xml.createElement('section')
		s1_node.setAttribute('name', 'Section 1')
		s1_node.setAttribute('id', 'section1')
		toolbox.appendChild(s1_node)
		s2_node = xml.createElement('section')
		s2_node.setAttribute('name', 'Section 2')
		s2_node.setAttribute('id', 'section2')
		toolbox.appendChild(s2_node)

		self.assertEqual(get_section_node('Section 1', xml), s1_node)
		self.assertEqual(get_section_node('Section 2', xml), s2_node)
		self.assertEqual(get_section_node('Section 3', xml), None)

	def test_exist_script_in_section(self):
		xml = Document()
		toolbox = xml.createElement('toolbox')
		xml.appendChild(toolbox)
		s1_node = xml.createElement('section')
		s1_node.setAttribute('name', 'Section 1')
		s1_node.setAttribute('id', 'section1')
		toolbox.appendChild(s1_node)
		tool_node = xml.createElement('tool')
		tool_node.setAttribute('file', 'section1/script1.xml')
		s1_node.appendChild(tool_node)
		tool_node = xml.createElement('tool')
		tool_node.setAttribute('file', 'section1/script2.xml')
		s1_node.appendChild(tool_node)
		s2_node = xml.createElement('section')
		s2_node.setAttribute('name', 'Section 2')
		s2_node.setAttribute('id', 'section2')
		toolbox.appendChild(s2_node)
		tool_node = xml.createElement('tool')
		tool_node.setAttribute('file', 'section2/script3.xml')
		s2_node.appendChild(tool_node)

		self.assertEqual(exist_script_in_section('script1.py', s1_node), True)
		self.assertEqual(exist_script_in_section('script2.py', s1_node), True)
		self.assertEqual(exist_script_in_section('script3.py', s1_node), False)
		self.assertEqual(exist_script_in_section('script1.py', s2_node), False)
		self.assertEqual(exist_script_in_section('script3.py', s2_node), True)
		self.assertEqual(exist_script_in_section('script4.py', s1_node), False)

	def test_add_section_to_xml(self):
		xml = Document()
		toolbox = xml.createElement('toolbox')
		xml.appendChild(toolbox)

		add_section_to_xml("Section 1", ['script1.py', 'script2.py'], xml)
		self.assertEqual(xml.toprettyxml(indent='\t'), exp_add_sect)

		add_section_to_xml("Section 2", [], xml)
		self.assertEqual(xml.toprettyxml(indent='\t'), exp_add_void_sect)

	def test_update_tool_conf_xml(self):
		xml = Document()
		toolbox = xml.createElement('toolbox')
		xml.appendChild(toolbox)
		section_dict = {"Section 1": ['script1.py', 'script2.py'],
			"Section 2": ['script3.py']}
		update_tool_conf_xml(xml, section_dict)
		self.assertEqual(xml.toprettyxml(indent='\t'), exp_update_1)

		section_dict["Section 3"] = ['script4.py', 'script5.py']
		update_tool_conf_xml(xml, section_dict)
		self.assertEqual(xml.toprettyxml(indent='\t'), exp_update_2)

	def test_integrate(self):
		scripts_dir = tempfile.mkdtemp(dir=self.tmp_dir)
		self._dirs_to_clean_up = [scripts_dir]
		copyfile(self.script1, path.join(scripts_dir, 'script1.py'))
		copyfile(self.script2, path.join(scripts_dir, 'script2.py'))
		copyfile(self.script3, path.join(scripts_dir, 'script3.py'))

		galaxy_dir = tempfile.mkdtemp(dir=self.tmp_dir)
		self._dirs_to_clean_up.append(galaxy_dir)
		galaxy_tool_conf_fp = path.join(galaxy_dir, 'tool_conf.xml')
		f = open(galaxy_tool_conf_fp, 'w')
		f.close()
		galaxy_tools_dir = path.join(galaxy_dir, 'tools')
		mkdir(galaxy_tools_dir)

		integrate(scripts_dir, galaxy_dir, self.config_file, False, None)

		self.assertTrue(path.exists(path.join(scripts_dir, 'integration.log')), "The log file was not create in the appropiate location")

		log_d, log_fp = tempfile.mkstemp(dir=self.tmp_dir)
		self._paths_to_clean_up = [log_fp]
		integrate(scripts_dir, galaxy_dir, self.config_file, True, log_fp)

		self.assertTrue(path.exists(log_fp), "The log file was not create in the appropiate location")


config_lines = """# At the begging we can have some comments
# More than one line comments
\tSection 1
script1.py
script2.py\toption1,option2

\tSection 2
script3.py
"""

bad_config_lines = """# One comment

script1.py
\tSection1
script2.py
"""

existing_tool_conf_lines = """<?xml version="1.0" ?>
<toolbox>
	<section id="exis_sect" name="Existing Section">
		<tool file="section_dir/file.xml"/>
	</section>
	<section id="getext" name="Get Data">
		<tool file="data_source/upload.xml"/>
	</section>
</toolbox>
"""

exp_doc_new = """<?xml version="1.0" ?>
<toolbox>
	<section id="getext" name="Get Data">
		<tool file="data_source/upload.xml"/>
	</section>
</toolbox>
"""

exp_doc_existing = """<?xml version="1.0" ?>
<toolbox>
\t
\t
\t<section id="exis_sect" name="Existing Section">
\t\t
\t\t
\t\t<tool file="section_dir/file.xml"/>
\t\t
\t
\t</section>
\t
\t
\t<section id="getext" name="Get Data">
\t\t
\t\t
\t\t<tool file="data_source/upload.xml"/>
\t\t
\t
\t</section>
\t

</toolbox>
"""

exp_add_sect = """<?xml version="1.0" ?>
<toolbox>
	<section id="section1" name="Section 1">
		<tool file="section1/script1.xml"/>
		<tool file="section1/script2.xml"/>
	</section>
</toolbox>
"""

exp_add_void_sect = """<?xml version="1.0" ?>
<toolbox>
	<section id="section1" name="Section 1">
		<tool file="section1/script1.xml"/>
		<tool file="section1/script2.xml"/>
	</section>
	<section id="section2" name="Section 2"/>
</toolbox>
"""

exp_update_1 = """<?xml version="1.0" ?>
<toolbox>
	<section id="section1" name="Section 1">
		<tool file="section1/script1.xml"/>
		<tool file="section1/script2.xml"/>
	</section>
	<section id="section2" name="Section 2">
		<tool file="section2/script3.xml"/>
	</section>
</toolbox>
"""

exp_update_2 = """<?xml version="1.0" ?>
<toolbox>
	<section id="section1" name="Section 1">
		<tool file="section1/script1.xml"/>
		<tool file="section1/script2.xml"/>
	</section>
	<section id="section2" name="Section 2">
		<tool file="section2/script3.xml"/>
	</section>
	<section id="section3" name="Section 3">
		<tool file="section3/script4.xml"/>
		<tool file="section3/script5.xml"/>
	</section>
</toolbox>
"""

if __name__ == '__main__':
	main()