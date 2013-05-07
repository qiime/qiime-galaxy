#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2011, The Galaxy-QIIME Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from qiime.pycogent_backports.option_parsing import make_option
from cogent.util.unit_test import TestCase, main
from xml.dom.minidom import Document
from xml_generator import OptionInfo, ScriptInfo, CommandGenerator, XmlOptionsAttributesGenerator, generate_xml_string, make_xml
import tempfile
from os import path, remove
from shutil import copyfile

class OptionInfoTest(TestCase):
    def setUp(self):
        pass

    def test_init(self):
        # Test of an option whithout short opt
        option = make_option('--example_opt', type='string',
                    help='Example string option')
        obs = OptionInfo(option)
        self.assertEqual(obs.name, 'example_opt')
        self.assertEqual(obs.type, 'text')
        self.assertEqual(obs.short_opt, None)
        self.assertEqual(obs.long_opt, '--example_opt')
        self.assertEqual(obs.label, 'Example string option')
        self.assertEqual(obs.default, None)
        self.assertEqual(obs.choices, None)
        self.assertEqual(obs.format, None)

        # Test of an option whithout long opt
        option = make_option('-e', type='string',
                    help='Example string option')
        obs = OptionInfo(option)
        self.assertEqual(obs.name, 'e')
        self.assertEqual(obs.type, 'text')
        self.assertEqual(obs.short_opt, '-e')
        self.assertEqual(obs.long_opt, None)
        self.assertEqual(obs.label, 'Example string option')
        self.assertEqual(obs.default, None)
        self.assertEqual(obs.choices, None)
        self.assertEqual(obs.format, None)

        # Tests of string option
        option = make_option('-e', '--example_opt', type='string',
                    help='Example string option')
        obs = OptionInfo(option)
        self.assertEqual(obs.name, 'example_opt')
        self.assertEqual(obs.type, 'text')
        self.assertEqual(obs.short_opt, '-e')
        self.assertEqual(obs.long_opt, '--example_opt')
        self.assertEqual(obs.label, 'Example string option')
        self.assertEqual(obs.default, None)
        self.assertEqual(obs.choices, None)
        self.assertEqual(obs.format, None)

        # Tests of int option
        option = make_option('-e', '--example_opt', type='int',
                    help='Example int option without default value')
        obs = OptionInfo(option)
        self.assertEqual(obs.name, 'example_opt')
        self.assertEqual(obs.type, 'integer')
        self.assertEqual(obs.short_opt, '-e')
        self.assertEqual(obs.long_opt, '--example_opt')
        self.assertEqual(obs.label, 'Example int option without default value')
        self.assertEqual(obs.default, None)
        self.assertEqual(obs.choices, None)
        self.assertEqual(obs.format, None)

        option = make_option('-e', '--example_opt', type='int', default=23,
                    help='Example int option with default value')
        obs = OptionInfo(option)
        self.assertEqual(obs.name, 'example_opt')
        self.assertEqual(obs.type, 'integer')
        self.assertEqual(obs.short_opt, '-e')
        self.assertEqual(obs.long_opt, '--example_opt')
        self.assertEqual(obs.label, 'Example int option with default value')
        self.assertEqual(obs.default, '23')
        self.assertEqual(obs.choices, None)
        self.assertEqual(obs.format, None)

        # Test of long option
        option = make_option('-e', '--example_opt', type='long', default=92233720368547758070,
                    help='Example long option with default value')
        obs = OptionInfo(option)
        self.assertEqual(obs.name, 'example_opt')
        self.assertEqual(obs.type, 'float')
        self.assertEqual(obs.short_opt, '-e')
        self.assertEqual(obs.long_opt, '--example_opt')
        self.assertEqual(obs.label, 'Example long option with default value')
        self.assertEqual(obs.default, '92233720368547758070')
        self.assertEqual(obs.choices, None)
        self.assertEqual(obs.format, None)

        # Test of float option
        option = make_option('-e', '--example_opt', type='float', default=23.45,
                    help='Example float option with default value')
        obs = OptionInfo(option)
        self.assertEqual(obs.name, 'example_opt')
        self.assertEqual(obs.type, 'float')
        self.assertEqual(obs.short_opt, '-e')
        self.assertEqual(obs.long_opt, '--example_opt')
        self.assertEqual(obs.label, 'Example float option with default value')
        self.assertEqual(obs.default, '23.45')
        self.assertEqual(obs.choices, None)
        self.assertEqual(obs.format, None)

        # Test of complex option
        option = make_option('-e', '--example_opt', type='complex',
                    help='Example complex option with default value')
        self.assertRaises(ValueError, OptionInfo, option)

        # Test of choice option
        option = make_option('-e', '--example_opt', type='choice', choices=['choice1','choice2','choice3'],
                    help='Example choice option')
        obs = OptionInfo(option)
        self.assertEqual(obs.name, 'example_opt')
        self.assertEqual(obs.type, 'select')
        self.assertEqual(obs.short_opt, '-e')
        self.assertEqual(obs.long_opt, '--example_opt')
        self.assertEqual(obs.label, 'Example choice option')
        self.assertEqual(obs.default, None)
        self.assertEqual(obs.choices, ['choice1','choice2','choice3'])
        self.assertEqual(obs.format, None) 

        # Test of existing_path option
        option = make_option('-e', '--example_opt', type='existing_path',
                    help='Example existing_path option')
        obs = OptionInfo(option)
        self.assertEqual(obs.name, 'example_opt')
        self.assertEqual(obs.type, 'input_dir')
        self.assertEqual(obs.short_opt, '-e')
        self.assertEqual(obs.long_opt, '--example_opt')
        self.assertEqual(obs.label, 'Example existing_path option')
        self.assertEqual(obs.default, None)
        self.assertEqual(obs.choices, None)
        self.assertEqual(obs.format, None) 

        # Test of new_path option
        option = make_option('-e', '--example_opt', type='new_path',
                    help='Example new_path option')
        obs = OptionInfo(option)
        self.assertEqual(obs.name, 'example_opt')
        self.assertEqual(obs.type, 'output_dir')
        self.assertEqual(obs.short_opt, '-e')
        self.assertEqual(obs.long_opt, '--example_opt')
        self.assertEqual(obs.label, 'Example new_path option')
        self.assertEqual(obs.default, None)
        self.assertEqual(obs.choices, None)
        self.assertEqual(obs.format, 'tgz')

        # Test of existing_filepath option
        option = make_option('-e', '--example_opt', type='existing_filepath',
                    help='Example existing_filepath option')
        obs = OptionInfo(option)
        self.assertEqual(obs.name, 'example_opt')
        self.assertEqual(obs.type, 'data')
        self.assertEqual(obs.short_opt, '-e')
        self.assertEqual(obs.long_opt, '--example_opt')
        self.assertEqual(obs.label, 'Example existing_filepath option')
        self.assertEqual(obs.default, None)
        self.assertEqual(obs.choices, None)
        self.assertEqual(obs.format, None)

        # Test of existing_filepaths option
        option = make_option('-e', '--example_opt', type='existing_filepaths',
                    help='Example existing_filepaths option')
        obs = OptionInfo(option)
        self.assertEqual(obs.name, 'example_opt')
        self.assertEqual(obs.type, 'repeat')
        self.assertEqual(obs.short_opt, '-e')
        self.assertEqual(obs.long_opt, '--example_opt')
        self.assertEqual(obs.label, 'Example existing_filepaths option')
        self.assertEqual(obs.default, None)
        self.assertEqual(obs.choices, None)
        self.assertEqual(obs.format, None)

        # Test of new_filepath option
        option = make_option('-e', '--example_opt', type='new_filepath',
                    help='Example new_filepath option')
        obs = OptionInfo(option)
        self.assertEqual(obs.name, 'example_opt')
        self.assertEqual(obs.type, 'output')
        self.assertEqual(obs.short_opt, '-e')
        self.assertEqual(obs.long_opt, '--example_opt')
        self.assertEqual(obs.label, 'Example new_filepath option')
        self.assertEqual(obs.default, None)
        self.assertEqual(obs.choices, None)
        self.assertEqual(obs.format, 'txt')

        # Test of existing_dirpath option
        option = make_option('-e', '--example_opt', type='existing_dirpath',
                    help='Example existing_dirpath option')
        obs = OptionInfo(option)
        self.assertEqual(obs.name, 'example_opt')
        self.assertEqual(obs.type, 'input_dir')
        self.assertEqual(obs.short_opt, '-e')
        self.assertEqual(obs.long_opt, '--example_opt')
        self.assertEqual(obs.label, 'Example existing_dirpath option')
        self.assertEqual(obs.default, None)
        self.assertEqual(obs.choices, None)
        self.assertEqual(obs.format, None)

        # Test of new_dirpath option
        option = make_option('-e', '--example_opt', type='new_dirpath',
                    help='Example new_dirpath option')
        obs = OptionInfo(option)
        self.assertEqual(obs.name, 'example_opt')
        self.assertEqual(obs.type, 'output_dir')
        self.assertEqual(obs.short_opt, '-e')
        self.assertEqual(obs.long_opt, '--example_opt')
        self.assertEqual(obs.label, 'Example new_dirpath option')
        self.assertEqual(obs.default, None)
        self.assertEqual(obs.choices, None)
        self.assertEqual(obs.format, 'tgz')

    def test_get_command_line_string(self):
        option = make_option('-e', '--example_opt', type='string',
                    help='Example string option')
        obj = OptionInfo(option)
        obs = obj.get_command_line_string()
        self.assertEqual(obs, '-e')

        # Test of an option whithout short opt
        option = make_option('--example_opt', type='string',
                    help='Example string option')
        obj = OptionInfo(option)
        obs = obj.get_command_line_string()
        self.assertEqual(obs, '--example_opt')

        # Test of an option whithout long opt
        option = make_option('-e', type='string',
                    help='Example string option')
        obj = OptionInfo(option)
        obs = obj.get_command_line_string()
        self.assertEqual(obs, '-e')

    def test_is_short_command_line(self):
        option = make_option('-e', '--example_opt', type='string',
                    help='Example string option')
        obj = OptionInfo(option)
        self.assertTrue(obj.is_short_command_line())

        # Test of an option whithout short opt
        option = make_option('--example_opt', type='string',
                    help='Example string option')
        obj = OptionInfo(option)
        self.assertFalse(obj.is_short_command_line())

        # Test of an option whithout long opt
        option = make_option('-e', type='string',
                    help='Example string option')
        obj = OptionInfo(option)
        self.assertTrue(obj.is_short_command_line())

    def test_has_default(self):
        option = make_option('-e', '--example_opt', type='int',
                    help='Example int option without default value')
        obs = OptionInfo(option)
        self.assertFalse(obs.has_default())

        option = make_option('-e', '--example_opt', type='int', default=23,
                    help='Example int option with default value')
        obs = OptionInfo(option)
        self.assertTrue(obs.has_default())

class ScriptInfoTest(TestCase):
    def setUp(self):
        self.info_dict = script_info_example

    def test_init(self):
        obs = ScriptInfo(self.info_dict, 'example_script', 'example_script.py')
        self.assertEqual(obs.id, 'example_script')
        self.assertEqual(obs.name, 'example script')
        self.assertEqual(obs.version, '1.4.0-dev')
        self.assertEqual(obs.description, 'An example of brief description')
        self.assertEqual(obs.help, 'An example of script description')
        self.assertEqual(obs.command, 'example_script.py')

        obs_option = obs.required_opts[0]
        self.assertEqual(obs_option.name, 'input_fp')
        self.assertEqual(obs_option.type, 'input_dir')
        self.assertEqual(obs_option.short_opt, '-i')
        self.assertEqual(obs_option.long_opt, '--input_fp')
        self.assertEqual(obs_option.label, 'An example of existing_path option')
        self.assertEqual(obs_option.default, None)
        self.assertEqual(obs_option.choices, None)
        self.assertEqual(obs_option.format, None)

        obs_option = obs.required_opts[1]
        self.assertEqual(obs_option.name, 'output_fp')
        self.assertEqual(obs_option.type, 'output_dir')
        self.assertEqual(obs_option.short_opt, '-o')
        self.assertEqual(obs_option.long_opt, '--output_fp')
        self.assertEqual(obs_option.label, 'An example of new_path option')
        self.assertEqual(obs_option.default, None)
        self.assertEqual(obs_option.choices, None)
        self.assertEqual(obs_option.format, 'tgz')

        obs_option = obs.optional_opts[0]
        self.assertEqual(obs_option.name, 'choice_ex')
        self.assertEqual(obs_option.type, 'select')
        self.assertEqual(obs_option.short_opt, '-c')
        self.assertEqual(obs_option.long_opt, '--choice_ex')
        self.assertEqual(obs_option.label, 'An example of choice option')
        self.assertEqual(obs_option.default, None)
        self.assertEqual(obs_option.choices, ['choice1','choice2','choice3'])
        self.assertEqual(obs_option.format, None)

        obs_option = obs.optional_opts[1]
        self.assertEqual(obs_option.name, 'repeat_ex')
        self.assertEqual(obs_option.type, 'repeat')
        self.assertEqual(obs_option.short_opt, '-r')
        self.assertEqual(obs_option.long_opt, '--repeat_ex')
        self.assertEqual(obs_option.label, 'An example of existing_filepaths option')
        self.assertEqual(obs_option.default, None)
        self.assertEqual(obs_option.choices, None)
        self.assertEqual(obs_option.format, None)

    def test_get_optional_opt(self):
        obj = ScriptInfo(self.info_dict, 'example_script', 'example_script.py')
        obs = obj._get_optional_opt('repeat_ex')
        self.assertEqual(obs.name, 'repeat_ex')
        self.assertEqual(obs.type, 'repeat')
        self.assertEqual(obs.short_opt, '-r')
        self.assertEqual(obs.long_opt, '--repeat_ex')
        self.assertEqual(obs.label, 'An example of existing_filepaths option')
        self.assertEqual(obs.default, None)
        self.assertEqual(obs.choices, None)
        self.assertEqual(obs.format, None)

        # This option does not exists
        obs = obj._get_optional_opt('option')
        self.assertEqual(obs, None)

        # This option is required
        obs = obj._get_optional_opt('input_fp')
        self.assertEqual(obs, None)

    def test_remove_options(self):
        obs = ScriptInfo(self.info_dict, 'example_script', 'example_script.py')
        obs.remove_options('choice_ex,repeat_ex')
        self.assertEqual(obs.optional_opts, [])

        obs = ScriptInfo(self.info_dict, 'example_script', 'example_script.py')
        obs.remove_options('choice_ex')
        self.assertEqual(len(obs.optional_opts), 1)
        obs_option = obs.optional_opts[0]
        self.assertEqual(obs_option.name, 'repeat_ex')
        self.assertEqual(obs_option.type, 'repeat')
        self.assertEqual(obs_option.short_opt, '-r')
        self.assertEqual(obs_option.long_opt, '--repeat_ex')
        self.assertEqual(obs_option.label, 'An example of existing_filepaths option')
        self.assertEqual(obs_option.default, None)
        self.assertEqual(obs_option.choices, None)
        self.assertEqual(obs_option.format, None)

        # Try to remove a required option
        obs = ScriptInfo(self.info_dict, 'example_script', 'example_script.py')
        self.assertRaises(ValueError, obs.remove_options, 'input_fp')

        # Try to remove an option which does not existss
        obs = ScriptInfo(self.info_dict, 'example_script', 'example_script.py')
        self.assertRaises(ValueError, obs.remove_options, 'option')

class CommandGeneratorTest(TestCase):
    def setUp(self):
        self.info = ScriptInfo(script_info_example, 'example_script', 'example_script.py')
        self.obj = CommandGenerator(self.info)

    def test_init(self):
        self.assertEqual(self.obj.info, self.info)
        self.assertEqual(self.obj.command_text, 'example_script.py')

    def test_update(self):
        self.obj.update()
        exp = "uncompress_tgz.py -i $input_fp -o example_script_input;\nexample_script.py -i example_script_input -o example_script_output\n#if str($choice_ex) != 'None':\n -c $choice_ex\n#end if\n\n#if $input_files_repeat_ex:\n\n#def list_dict_to_string(list_dict):\n\t#set $file_list = list_dict[0]['additional_input'].__getattr__('file_name')\n\t#for d in list_dict[1:]:\n\t\t#set $file_list = $file_list + ',' + d['additional_input'].__getattr__('file_name')\n\t#end for\n\t#return $file_list\n#end def\n -r $list_dict_to_string($input_files_repeat_ex)\n#end if\n;\ncompress_path.py -i example_script_output -o $output_fp\n"
        self.assertEqual(self.obj.command_text, exp)

    def test_generate_text_command_text(self):
        obj_info = ScriptInfo(text_script_info, 'text_script', 'text_script.py')
        obj = CommandGenerator(obj_info)

        obj._generate_text_command_text(obj_info.required_opts[0])
        exp = 'text_script.py -s $string'
        self.assertEqual(obj.command_text, exp)

        obj._is_optional = True
        obj._generate_text_command_text(obj_info.optional_opts[0])
        exp = 'text_script.py -s $string\n#if str($text):\n --text=$text\n#end if\n'
        self.assertEqual(obj.command_text, exp)

    def test_generate_data_select_command_text(self):
        obj_info = ScriptInfo(data_select_script_info, 'data_select_script', 'data_select_script.py')
        obj = CommandGenerator(obj_info)

        obj._generate_data_select_command_text(obj_info.required_opts[0])
        exp = 'data_select_script.py --input_fp=$input_fp'
        self.assertEqual(obj.command_text, exp)

        obj._is_optional = True
        obj._generate_data_select_command_text(obj_info.optional_opts[0])
        exp = "data_select_script.py --input_fp=$input_fp\n#if str($choice) != 'None':\n -c $choice\n#end if\n"
        self.assertEqual(obj.command_text, exp)

    def test_generate_integer_float_command_text(self):
        obj_info = ScriptInfo(integer_float_script_info, 'int_float_script', 'int_float_script.py')
        obj = CommandGenerator(obj_info)

        obj._generate_integer_float_command_text(obj_info.required_opts[0])
        exp = "int_float_script.py -i $integer"
        self.assertEqual(obj.command_text, exp)

        obj._is_optional = True
        obj._generate_integer_float_command_text(obj_info.optional_opts[0])
        exp = "int_float_script.py -i $integer\n#if $float:\n --float=$float\n#end if\n"
        self.assertEqual(obj.command_text, exp)

    def test_generate_boolean_command_text(self):
        obj_info = ScriptInfo(boolean_script_info, 'boolean_script', 'boolean_script.py')
        obj = CommandGenerator(obj_info)

        obj._is_optional = True
        obj._generate_boolean_command_text(obj_info.optional_opts[0])
        exp = "boolean_script.py\n#if $true_boolean:\n -t\n#end if\n"
        self.assertEqual(obj.command_text, exp)

        obj._generate_boolean_command_text(obj_info.optional_opts[1])
        exp = "boolean_script.py\n#if $true_boolean:\n -t\n#end if\n\n#if $false_boolean:\n --false_boolean\n#end if\n"
        self.assertEqual(obj.command_text, exp)

    def test_generate_repeat_command_text(self):
        obj_info = ScriptInfo(repeat_script_info, 'repeat_script', 'repeat_script.py')
        obj = CommandGenerator(obj_info)

        obj._generate_repeat_command_text(obj_info.required_opts[0])
        exp = "repeat_script.py\n#def list_dict_to_string(list_dict):\n\t#set $file_list = list_dict[0]['additional_input'].__getattr__('file_name')\n\t#for d in list_dict[1:]:\n\t\t#set $file_list = $file_list + ',' + d['additional_input'].__getattr__('file_name')\n\t#end for\n\t#return $file_list\n#end def\n -i $list_dict_to_string($input_files_input_fps)"
        self.assertEqual(obj.command_text, exp)

        obj._is_optional = True
        obj._generate_repeat_command_text(obj_info.optional_opts[0])
        exp = "repeat_script.py\n#def list_dict_to_string(list_dict):\n\t#set $file_list = list_dict[0]['additional_input'].__getattr__('file_name')\n\t#for d in list_dict[1:]:\n\t\t#set $file_list = $file_list + ',' + d['additional_input'].__getattr__('file_name')\n\t#end for\n\t#return $file_list\n#end def\n -i $list_dict_to_string($input_files_input_fps)\n#if $input_files_repeat:\n --repeat=$list_dict_to_string($input_files_repeat)\n#end if\n"
        self.assertEqual(obj.command_text, exp)

    def test_generate_output_command_text(self):
        obj_info = ScriptInfo(output_script_info, 'output_script', 'output_script.py')
        obj = CommandGenerator(obj_info)

        obj._generate_output_command_text(obj_info.required_opts[0])
        exp = "output_script.py -o $output_fp"
        self.assertEqual(obj.command_text, exp)

        obj._is_optional = True
        obj._generate_output_command_text(obj_info.optional_opts[0])
        exp = "output_script.py -o $output_fp --new_filepath=$new_filepath"
        self.assertEqual(obj.command_text, exp)

    def test_generate_output_dir_command_text(self):
        obj_info = ScriptInfo(output_dir_script_info, 'output_dir_script', 'output_dir_script.py')
        obj = CommandGenerator(obj_info)

        obj._generate_output_dir_command_text(obj_info.required_opts[0])
        exp = "output_dir_script.py -p output_dir_script_output"
        self.assertEqual(obj.command_text, exp)

        obj_info = ScriptInfo(output_dir_script_info, 'output_dir_script', 'output_dir_script.py')
        obj = CommandGenerator(obj_info)

        obj._is_optional = True
        obj._generate_output_dir_command_text(obj_info.optional_opts[0])
        exp = "output_dir_script.py -d output_dir_script_output"
        self.assertEqual(obj.command_text, exp)

        obj._is_optional = False
        self.assertRaises(ValueError, obj._generate_output_dir_command_text, obj_info.required_opts[0])

    def test_generate_input_dir_command_text(self):
        obj_info = ScriptInfo(input_dir_script_info, 'input_dir_script', 'input_dir_script.py')
        obj = CommandGenerator(obj_info)

        obj._generate_input_dir_command_text(obj_info.required_opts[0])
        exp = "input_dir_script.py -p input_dir_script_input"
        self.assertEqual(obj.command_text, exp)

        obj_info = ScriptInfo(input_dir_script_info, 'input_dir_script', 'input_dir_script.py')
        obj = CommandGenerator(obj_info)

        self._is_optional = True
        obj._generate_input_dir_command_text(obj_info.optional_opts[0])
        exp = "input_dir_script.py -d input_dir_script_input"
        self.assertEqual(obj.command_text, exp)

        obj._is_optional = False
        self.assertRaises(ValueError, obj._generate_input_dir_command_text, obj_info.required_opts[0])

class XmlOptionsAttributesGeneratorTest(TestCase):
    def setUp(self):
        pass

    def test_update(self):
        info = ScriptInfo(script_info_example, 'example_script', 'example_script.py')
        doc = Document()
        tool = doc.createElement('tool')
        doc.appendChild(tool)
        inputs = doc.createElement('inputs')
        outputs = doc.createElement('outputs')
        tool.appendChild(inputs)
        tool.appendChild(outputs)

        xml_opts_generator = XmlOptionsAttributesGenerator(info, doc, inputs, outputs)
        xml_opts_generator.update()
        obs = doc.toprettyxml(indent="\t")
        self.assertEqual(obs, exp_update)

    def test_generate_integer_float_attributes(self):
        info = ScriptInfo(integer_float_script_info, 'integer_float_script', 'integer_float_script.py')
        doc = Document()
        tool = doc.createElement('tool')
        doc.appendChild(tool)
        inputs = doc.createElement('inputs')
        outputs = doc.createElement('outputs')
        tool.appendChild(inputs)
        tool.appendChild(outputs)

        xml_opts_generator = XmlOptionsAttributesGenerator(info, doc, inputs, outputs)

        xml_opts_generator._generate_integer_float_attributes(info.required_opts[0])
        obs = doc.toprettyxml(indent="\t")
        self.assertEqual(obs, exp_integer_float_1)

        xml_opts_generator._is_optional = True
        xml_opts_generator._generate_integer_float_attributes(info.optional_opts[0])
        obs = doc.toprettyxml(indent="\t")
        self.assertEqual(obs, exp_integer_float_2)

    def test_generate_text_data_attributes(self):
        info = ScriptInfo(text_data_script_info, 'param_script', 'param_script.py')
        doc = Document()
        tool = doc.createElement('tool')
        doc.appendChild(tool)
        inputs = doc.createElement('inputs')
        outputs = doc.createElement('outputs')
        tool.appendChild(inputs)
        tool.appendChild(outputs)

        xml_opts_generator = XmlOptionsAttributesGenerator(info, doc, inputs, outputs)

        xml_opts_generator._generate_text_data_attributes(info.required_opts[0])
        obs = doc.toprettyxml(indent="\t")
        self.assertEqual(obs, exp_text_data_1)

        xml_opts_generator._is_optional = True
        xml_opts_generator._generate_text_data_attributes(info.optional_opts[0])
        obs = doc.toprettyxml(indent="\t")
        self.assertEqual(obs, exp_text_data_2)

    def test_generate_input_dir_attributes(self):
        info = ScriptInfo(input_dir_script_info, 'input_dir_script', 'input_dir_script.py')
        doc = Document()
        tool = doc.createElement('tool')
        doc.appendChild(tool)
        inputs = doc.createElement('inputs')
        outputs = doc.createElement('outputs')
        tool.appendChild(inputs)
        tool.appendChild(outputs)

        xml_opts_generator = XmlOptionsAttributesGenerator(info, doc, inputs, outputs)

        xml_opts_generator._generate_input_dir_attributes(info.required_opts[0])
        obs = doc.toprettyxml(indent="\t")
        self.assertEqual(obs, exp_input_dir)

    def test_generate_select_attributes(self):
        info = ScriptInfo(select_XML_script_info, 'select_script', 'select_script.py')
        doc = Document()
        tool = doc.createElement('tool')
        doc.appendChild(tool)
        inputs = doc.createElement('inputs')
        outputs = doc.createElement('outputs')
        tool.appendChild(inputs)
        tool.appendChild(outputs)

        xml_opts_generator = XmlOptionsAttributesGenerator(info, doc, inputs, outputs)

        xml_opts_generator._generate_select_attributes(info.required_opts[0])
        obs = doc.toprettyxml(indent="\t")
        self.assertEqual(obs, exp_select_1)

        xml_opts_generator._is_optional = True
        xml_opts_generator._generate_select_attributes(info.optional_opts[0])
        obs = doc.toprettyxml(indent="\t")
        self.assertEqual(obs, exp_select_2)

    def test_generate_multiple_select_attributes(self):
        info = ScriptInfo(multiple_select_XML_script_info, 'multiple_select_script', 'multiple_select_script.py')
        doc = Document()
        tool = doc.createElement('tool')
        doc.appendChild(tool)
        inputs = doc.createElement('inputs')
        outputs = doc.createElement('outputs')
        tool.appendChild(inputs)
        tool.appendChild(outputs)

        xml_opts_generator = XmlOptionsAttributesGenerator(info, doc, inputs, outputs)

        xml_opts_generator._generate_multiple_select_attributes(info.required_opts[0])
        obs = doc.toprettyxml(indent="\t")
        self.assertEqual(obs, exp_multiple_select)

    def test_generate_repeat_attributes(self):
        info = ScriptInfo(repeat_script_info, 'repeat_script', 'repeat_script.py')
        doc = Document()
        tool = doc.createElement('tool')
        doc.appendChild(tool)
        inputs = doc.createElement('inputs')
        outputs = doc.createElement('outputs')
        tool.appendChild(inputs)
        tool.appendChild(outputs)

        xml_opts_generator = XmlOptionsAttributesGenerator(info, doc, inputs, outputs)

        xml_opts_generator._generate_repeat_attributes(info.required_opts[0])
        obs = doc.toprettyxml(indent="\t")
        self.assertEqual(obs, exp_repeat_1)

        xml_opts_generator._is_optional = True
        xml_opts_generator._generate_repeat_attributes(info.optional_opts[0])
        obs = doc.toprettyxml(indent="\t")
        self.assertEqual(obs, exp_repeat_2)

    def test_generate_output_attributes(self):
        info = ScriptInfo(output_XML_script_info, 'output_script', 'output_script.py')
        doc = Document()
        tool = doc.createElement('tool')
        doc.appendChild(tool)
        inputs = doc.createElement('inputs')
        outputs = doc.createElement('outputs')
        tool.appendChild(inputs)
        tool.appendChild(outputs)

        xml_opts_generator = XmlOptionsAttributesGenerator(info, doc, inputs, outputs)

        xml_opts_generator._generate_output_attributes(info.required_opts[0])
        obs = doc.toprettyxml(indent="\t")
        self.assertEqual(obs, exp_output_1)

        xml_opts_generator._is_optional = True
        xml_opts_generator._generate_output_attributes(info.optional_opts[0])
        obs = doc.toprettyxml(indent="\t")
        self.assertEqual(obs, exp_output_2)

    def test_generate_boolean_attributes(self):
        info = ScriptInfo(boolean_script_info, 'boolean_script', 'boolean_script.py')
        doc = Document()
        tool = doc.createElement('tool')
        doc.appendChild(tool)
        inputs = doc.createElement('inputs')
        outputs = doc.createElement('outputs')
        tool.appendChild(inputs)
        tool.appendChild(outputs)

        xml_opts_generator = XmlOptionsAttributesGenerator(info, doc, inputs, outputs)

        xml_opts_generator._is_optional = True
        xml_opts_generator._generate_boolean_attributes(info.optional_opts[0])
        obs = doc.toprettyxml(indent="\t")
        self.assertEqual(obs, exp_boolean_1)

        xml_opts_generator._generate_boolean_attributes(info.optional_opts[1])
        obs = doc.toprettyxml(indent="\t")
        self.assertEqual(obs, exp_boolean_2)

class XmlGeneratorTest(TestCase):
    def setUp(self):
        self.info = ScriptInfo(script_info_example, 'example_script', 'example_script.py')
        self.script_fp = './support_files/example_script.py'
        self.output_dir = tempfile.gettempdir()

        self._paths_to_clean_up = []

    def tearDown(self):
        map(remove, self._paths_to_clean_up)

    def test_generate_xml_string(self):
        obs = generate_xml_string(self.info)
        self.assertEqual(obs, exp_full_xml)

    def test_make_xml(self):
        output_fp = path.join(self.output_dir, 'example_script.xml')
        self._paths_to_clean_up = [output_fp, './example_script.py']
        copyfile(self.script_fp, './example_script.py')

        make_xml(self.script_fp, self.output_dir, None)

        self.assertTrue(path.exists(output_fp), 'The xml file was not created in the appropiate location')

# A script info example
script_info_example = {}
script_info_example['brief_description'] = "An example of brief description"
script_info_example['script_description'] = "An example of script description"
script_info_example['script_usage'] = [("Example", "Field not used", "%prog ")]
script_info_example['output_description'] = "Field not used"
script_info_example['required_options'] = [
    make_option('-i', '--input_fp', type="existing_path",
                help='An example of existing_path option'),
    make_option('-o', '--output_fp', type="new_path",
                help='An example of new_path option')
]
script_info_example['optional_options'] = [
    make_option('-c', '--choice_ex', type="choice", choices=['choice1','choice2','choice3'],
                help='An example of choice option'),
    make_option('-r', '--repeat_ex', type="existing_filepaths",
                help='An example of existing_filepaths option')
]
script_info_example['version'] = "1.4.0-dev"

text_script_info = {}
text_script_info['brief_description'] = "Example of script info with string options"
text_script_info['script_description'] = "An example of script info with a required string option and an optional string option"
text_script_info['script_usage'] = [("Example", "Field not used", "%prog ")]
text_script_info['output_description'] = "Field not used"
text_script_info['required_options'] = [
    make_option('-s', '--string', type="string",
        help="An example of required text option"),
]
text_script_info['optional_options'] = [
    make_option('--text', type="string",
        help="An example of optional text option"),
]
text_script_info['version'] = "1.4.0-dev"

integer_float_script_info = {}
integer_float_script_info['brief_description'] = "Example of script info with int and float options"
integer_float_script_info['script_description'] = "An example of script info with a required int option and an optional float option"
integer_float_script_info['script_usage'] = [("Example", "Field not used", "%prog ")]
integer_float_script_info['output_description'] = "Field not used"
integer_float_script_info['required_options'] = [
    make_option('-i', '--integer', type="int",
        help="An example of required integer option"),
]
integer_float_script_info['optional_options'] = [
    make_option('--float', type="float",
        help="An example of optional float option"),
]
integer_float_script_info['version'] = "1.4.0-dev"

data_select_script_info = {}
data_select_script_info['brief_description'] = "Example of script info with existing_filepath and choice options"
data_select_script_info['script_description'] = "An example of script info with a required existing_filepath option and an optional choice option"
data_select_script_info['script_usage'] = [("Example", "Field not used", "%prog ")]
data_select_script_info['output_description'] = "Field not used"
data_select_script_info['required_options'] = [
    make_option('--input_fp', type='existing_filepath',
        help="An example of required existing_filepath option")
]
data_select_script_info['optional_options'] = [
    make_option('-c', '--choice', type='choice', choices=['choice1', 'choice2', 'choice3'],
        help="An example of optional choice option")
]
data_select_script_info['version'] = "1.4.0-dev"

input_dir_script_info = {}
input_dir_script_info['brief_description'] = "Example of script info with existing_path and existing_dirpath options"
input_dir_script_info['script_description'] = "An example of script info with a required existing_path option and an optional existing_dirpath option"
input_dir_script_info['script_usage'] = [("Example", "Field not used", "%prog ")]
input_dir_script_info['output_description'] = "Field not used"
input_dir_script_info['required_options'] = [
    make_option('-p', '--path', type='existing_path',
        help="An example of required existing_path option")
]
input_dir_script_info['optional_options'] = [
    make_option('-d', '--dir_path', type='existing_dirpath',
        help="An example of required existing_dirpath option")
]
input_dir_script_info['version'] = "1.4.0-dev"

repeat_script_info = {}
repeat_script_info['brief_description'] = "Example of script info with existing_filepaths options"
repeat_script_info['script_description'] = "An example of script info with a required existing_filepaths option and an optional existing_filepaths option"
repeat_script_info['script_usage'] = [("Example", "Field not used", "%prog ")]
repeat_script_info['output_description'] = "Field not used"
repeat_script_info['required_options'] = [
    make_option('-i', '--input_fps', type='existing_filepaths',
        help="An example of required existing_filepaths option")
]
repeat_script_info['optional_options'] = [
    make_option('--repeat', type='existing_filepaths',
        help="An example of optional existing_filepaths option")
]
repeat_script_info['version'] = "1.4.0-dev"

output_script_info = {}
output_script_info['brief_description'] = "Example of script info with new_filepath options"
output_script_info['script_description'] = "An example of script info with a required new_filepath option and an optional new_filepath option"
output_script_info['script_usage'] = [("Example", "Field not used", "%prog ")]
output_script_info['output_description'] = "Field not used"
output_script_info['required_options'] = [
    make_option('-o', '--output_fp', type='new_filepath',
        help="An example of required new_filepath option")
]
output_script_info['optional_options'] = [
    make_option('--new_filepath', type='new_filepath',
        help="An example of optional new_filepath option")
]
output_script_info['version'] = "1.4.0-dev"

output_dir_script_info = {}
output_dir_script_info['brief_description'] = "Example of script info with new_path and new_dirpath options"
output_dir_script_info['script_description'] = "An example of script info with a required new_path option and an optional new_dirpath option"
output_dir_script_info['script_usage'] = [("Example", "Field not used", "%prog ")]
output_dir_script_info['output_description'] = "Field not used"
output_dir_script_info['required_options'] = [
    make_option('-p', '--new_path', type='new_path',
        help="An example of required new_path option")
]
output_dir_script_info['optional_options'] = [
    make_option('-d', '--new_dirpath', type='new_dirpath',
        help="An example of optional new_dirpath option")
]
output_dir_script_info['version'] = "1.4.0-dev"

boolean_script_info = {}
boolean_script_info['brief_description'] = "Example of script info with boolean options"
boolean_script_info['script_description'] = "An example of script info with an optional boolean option (a boolean option never is required)"
boolean_script_info['script_usage'] = [("Example", "Field not used", "%prog ")]
boolean_script_info['output_description'] = "Field not used"
boolean_script_info['required_options'] = []
boolean_script_info['optional_options'] = [
    make_option('-t', '--true_boolean', action='store_true',
        help="An example of boolean option"),
    make_option('--false_boolean', action='store_false',
        help="An example of boolean option")
]
boolean_script_info['version'] = "1.4.0-dev"

text_data_script_info = {}
text_data_script_info['brief_description'] = "Example of script info with string, int, float and existing_filepath options"
text_data_script_info['script_description'] = "An example of script info with a required string option, a required int option, an optional float option and an optional existing_filepath option"
text_data_script_info['script_usage'] = [("Example", "Field not used", "%prog ")]
text_data_script_info['output_description'] = "Field not used"
text_data_script_info['required_options'] = [
    make_option('-s', '--string', type="string", default="some_value",
        help="An example of required text option [default: %default]")
]
text_data_script_info['optional_options'] = [
    make_option('--input_fp', type='existing_filepath',
        help="An example of optional existing_filepath option")
]
text_data_script_info['version'] = "1.4.0-dev"

select_XML_script_info = {}
select_XML_script_info['brief_description'] = "Example of script info with a choice options"
select_XML_script_info['script_description'] = "An example of script info with a required choice option and an optional choice option"
select_XML_script_info['script_usage'] = [("Example", "Field not used", "%prog ")]
select_XML_script_info['output_description'] = "Field not used"
select_XML_script_info['required_options'] = [
    make_option('-c', '--choice', type='choice', choices=['choice1', 'choice2', 'choice3'],
        help="An example of required choice option")
]
select_XML_script_info['optional_options'] = [
    make_option('-s', '--select', type='choice', choices=['choice1', 'choice2', 'choice3'],
        help="An example of optional choice option")
]
select_XML_script_info['version'] = "1.4.0-dev"

multiple_select_XML_script_info = {}
multiple_select_XML_script_info['brief_description'] = "Example of script info with a choice options"
multiple_select_XML_script_info['script_description'] = "An example of script info with a required choice option and an optional choice option"
multiple_select_XML_script_info['script_usage'] = [("Example", "Field not used", "%prog ")]
multiple_select_XML_script_info['output_description'] = "Field not used"
multiple_select_XML_script_info['required_options'] = [
    make_option('-c', '--choice', type='multiple_choice', mchoices=['choice1', 'choice2', 'choice3'],
        help="An example of required choice option")
]
multiple_select_XML_script_info['optional_options'] = []
multiple_select_XML_script_info['version'] = "1.4.0-dev"

output_XML_script_info = {}
output_XML_script_info['brief_description'] = "Example of script info with new_path and new_filepath options"
output_XML_script_info['script_description'] = "An example of script info with a required new_path and an optional new_filepath option"
output_XML_script_info['script_usage'] = [("Example", "Field not used", "%prog ")]
output_XML_script_info['output_description'] = "Field not used"
output_XML_script_info['required_options'] = [
    make_option('-p', '--new_path', type='new_path',
        help="An example of required new_path option")
]
output_XML_script_info['optional_options'] = [
    make_option('--new_filepath', type='new_filepath',
        help="An example of optional new_filepath option")
]
output_XML_script_info['version'] = "1.4.0-dev"

exp_integer_float_1 = """<?xml version="1.0" ?>
<tool>
\t<inputs>
\t\t<param label="An example of required integer option" name="integer" optional="False" type="integer" value="0"/>
\t</inputs>
\t<outputs/>
</tool>
"""

exp_integer_float_2 = """<?xml version="1.0" ?>
<tool>
\t<inputs>
\t\t<param label="An example of required integer option" name="integer" optional="False" type="integer" value="0"/>
\t\t<param label="An example of optional float option" name="float" optional="True" type="float"/>
\t</inputs>
\t<outputs/>
</tool>
"""

exp_text_data_1 = """<?xml version="1.0" ?>
<tool>
\t<inputs>
\t\t<param default="some_value" label="An example of required text option [default: some_value]" name="string" optional="False" type="text"/>
\t</inputs>
\t<outputs/>
</tool>
"""

exp_text_data_2 = """<?xml version="1.0" ?>
<tool>
\t<inputs>
\t\t<param default="some_value" label="An example of required text option [default: some_value]" name="string" optional="False" type="text"/>
\t\t<param label="An example of optional existing_filepath option" name="input_fp" optional="True" type="data"/>
\t</inputs>
\t<outputs/>
</tool>
"""

exp_input_dir = """<?xml version="1.0" ?>
<tool>
\t<inputs>
\t\t<param label="An example of required existing_path option" name="path" type="data"/>
\t</inputs>
\t<outputs/>
</tool>
"""

exp_select_1 = """<?xml version="1.0" ?>
<tool>
\t<inputs>
\t\t<param label="An example of required choice option" name="choice" optional="False" type="select">
\t\t\t<option value="choice1">
\t\t\t\tchoice1
\t\t\t</option>
\t\t\t<option value="choice2">
\t\t\t\tchoice2
\t\t\t</option>
\t\t\t<option value="choice3">
\t\t\t\tchoice3
\t\t\t</option>
\t\t</param>
\t</inputs>
\t<outputs/>
</tool>
"""

exp_select_2 = """<?xml version="1.0" ?>
<tool>
\t<inputs>
\t\t<param label="An example of required choice option" name="choice" optional="False" type="select">
\t\t\t<option value="choice1">
\t\t\t\tchoice1
\t\t\t</option>
\t\t\t<option value="choice2">
\t\t\t\tchoice2
\t\t\t</option>
\t\t\t<option value="choice3">
\t\t\t\tchoice3
\t\t\t</option>
\t\t</param>
\t\t<param label="An example of optional choice option" name="select" optional="True" type="select">
\t\t\t<option selected="True" value="None">
\t\t\t\tSelection is Optional
\t\t\t</option>
\t\t\t<option value="choice1">
\t\t\t\tchoice1
\t\t\t</option>
\t\t\t<option value="choice2">
\t\t\t\tchoice2
\t\t\t</option>
\t\t\t<option value="choice3">
\t\t\t\tchoice3
\t\t\t</option>
\t\t</param>
\t</inputs>
\t<outputs/>
</tool>
"""

exp_multiple_select = """<?xml version="1.0" ?>
<tool>
\t<inputs>
\t\t<param label="An example of required choice option" multiple="True" name="choice" optional="False" type="select">
\t\t\t<option value="choice1">
\t\t\t\tchoice1
\t\t\t</option>
\t\t\t<option value="choice2">
\t\t\t\tchoice2
\t\t\t</option>
\t\t\t<option value="choice3">
\t\t\t\tchoice3
\t\t\t</option>
\t\t</param>
\t</inputs>
\t<outputs/>
</tool>
"""

exp_repeat_1 = """<?xml version="1.0" ?>
<tool>
\t<inputs>
\t\t<repeat name="input_files_input_fps" optional="False" title="input_fps">
\t\t\t<param label="An example of required existing_filepaths option" name="additional_input" type="data"/>
\t\t</repeat>
\t</inputs>
\t<outputs/>
</tool>
"""

exp_repeat_2 = """<?xml version="1.0" ?>
<tool>
\t<inputs>
\t\t<repeat name="input_files_input_fps" optional="False" title="input_fps">
\t\t\t<param label="An example of required existing_filepaths option" name="additional_input" type="data"/>
\t\t</repeat>
\t\t<repeat name="input_files_repeat" optional="True" title="repeat">
\t\t\t<param label="An example of optional existing_filepaths option" name="additional_input" type="data"/>
\t\t</repeat>
\t</inputs>
\t<outputs/>
</tool>
"""

exp_output_1 = """<?xml version="1.0" ?>
<tool>
\t<inputs/>
\t<outputs>
\t\t<data format="tgz" name="new_path"/>
\t</outputs>
</tool>
"""

exp_output_2 = """<?xml version="1.0" ?>
<tool>
\t<inputs/>
\t<outputs>
\t\t<data format="tgz" name="new_path"/>
\t\t<data format="txt" name="new_filepath"/>
\t</outputs>
</tool>
"""

exp_boolean_1 = """<?xml version="1.0" ?>
<tool>
\t<inputs>
\t\t<param label="An example of boolean option" name="true_boolean" selected="False" type="boolean"/>
\t</inputs>
\t<outputs/>
</tool>
"""

exp_boolean_2 = """<?xml version="1.0" ?>
<tool>
\t<inputs>
\t\t<param label="An example of boolean option" name="true_boolean" selected="False" type="boolean"/>
\t\t<param label="An example of boolean option" name="false_boolean" selected="False" type="boolean"/>
\t</inputs>
\t<outputs/>
</tool>
"""

exp_update = """<?xml version="1.0" ?>
<tool>
\t<inputs>
\t\t<param label="An example of existing_path option" name="input_fp" type="data"/>
\t\t<param label="An example of choice option" name="choice_ex" optional="True" type="select">
\t\t\t<option selected="True" value="None">
\t\t\t\tSelection is Optional
\t\t\t</option>
\t\t\t<option value="choice1">
\t\t\t\tchoice1
\t\t\t</option>
\t\t\t<option value="choice2">
\t\t\t\tchoice2
\t\t\t</option>
\t\t\t<option value="choice3">
\t\t\t\tchoice3
\t\t\t</option>
\t\t</param>
\t\t<repeat name="input_files_repeat_ex" optional="True" title="repeat_ex">
\t\t\t<param label="An example of existing_filepaths option" name="additional_input" type="data"/>
\t\t</repeat>
\t</inputs>
\t<outputs>
\t\t<data format="tgz" name="output_fp"/>
\t</outputs>
</tool>
"""

exp_full_xml ="""<?xml version="1.0" ?>
<tool id="example_script" name="example script" version="1.4.0-dev">
\t<description>
\t\tAn example of brief description
\t</description>
\t<requirements>
\t\t<requirement type="package">qiime</requirement>
\t</requirements>
\t<command>
\t\tuncompress_tgz.py -i $input_fp -o example_script_input;
example_script.py -i example_script_input -o example_script_output
#if str($choice_ex) != 'None':
 -c $choice_ex
#end if

#if $input_files_repeat_ex:

#def list_dict_to_string(list_dict):
\t#set $file_list = list_dict[0]['additional_input'].__getattr__('file_name')
\t#for d in list_dict[1:]:
\t\t#set $file_list = $file_list + ',' + d['additional_input'].__getattr__('file_name')
\t#end for
\t#return $file_list
#end def
 -r $list_dict_to_string($input_files_repeat_ex)
#end if
;
compress_path.py -i example_script_output -o $output_fp

\t</command>
\t<inputs>
\t\t<param label="An example of existing_path option" name="input_fp" type="data"/>
\t\t<param label="An example of choice option" name="choice_ex" optional="True" type="select">
\t\t\t<option selected="True" value="None">
\t\t\t\tSelection is Optional
\t\t\t</option>
\t\t\t<option value="choice1">
\t\t\t\tchoice1
\t\t\t</option>
\t\t\t<option value="choice2">
\t\t\t\tchoice2
\t\t\t</option>
\t\t\t<option value="choice3">
\t\t\t\tchoice3
\t\t\t</option>
\t\t</param>
\t\t<repeat name="input_files_repeat_ex" optional="True" title="repeat_ex">
\t\t\t<param label="An example of existing_filepaths option" name="additional_input" type="data"/>
\t\t</repeat>
\t</inputs>
\t<outputs>
\t\t<data format="tgz" name="output_fp"/>
\t</outputs>
\t<help>
\t\tAn example of script description
\t</help>
</tool>
"""

if __name__ == '__main__':
    main()
