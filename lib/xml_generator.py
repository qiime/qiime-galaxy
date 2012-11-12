#!/usr/bin/env python

"""
	Generate a xml file for the Galaxy integration from a QIIME python script
"""

__author__ = "Jose Antonio Navas"
__copyright__ = "Copyright 2011, The QIIME Project"
__credits__ = ["Jose Antonio Navas"]
__license__ = "GPL"
__version__ = "1.4.0-dev"
__maintainer__ = "Jose Antonio Navas"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from os.path import splitext, split, join
from os import remove
from xml.dom.minidom import Document

# Dict used for convert the cogent.util.option_parsing.CogentOption.TYPES to Galaxy types
type_converter = {}
type_converter['string'] = "text"
type_converter['int'] = "integer"
type_converter['long'] = "float"
type_converter['float'] = "float"
type_converter['choice'] = "select"
type_converter['multiple_choice'] = "multiple_select"
type_converter['existing_filepath'] = "data"
type_converter['existing_filepaths'] = "repeat"
type_converter['existing_dirpath'] = "input_dir"
type_converter['existing_path'] = "input_dir"
type_converter['new_filepath'] = "output"
type_converter['new_dirpath'] = "output_dir"
type_converter['new_path'] = "output_dir"

# Definitions for the command text
COMMAND_LINE_COMPRESS = ";\ncompress_path.py -i %s -o $%s\n"
COMMAND_LINE_UNCOMPRESS = "uncompress_tgz.py -i $%s -o %s;\n"
LIST_DICT_TO_STRING_FUNCTION = """
#def list_dict_to_string(list_dict):
	#set $file_list = list_dict[0]['additional_input'].__getattr__('file_name')
	#for d in list_dict[1:]:
		#set $file_list = $file_list + ',' + d['additional_input'].__getattr__('file_name')
	#end for
	#return $file_list
#end def
"""

class OptionInfo(object):
	"""
		Class for a what an option is from Galaxy's XML point of view

		A cogent.util.option_parsing.CogentOption must be given
	"""
	def __init__(self, option):
		self.name = option.get_opt_string().replace("-", "")

		# Type boolean is not defined on cogent.util.option_parsing.CogentOption.TYPES
		# The only way to know if it is boolean or not is looking at the action attribute
		try:
			self.type = "boolean" if option.action in ['store_true', 'store_false'] else type_converter[option.type]
		except KeyError:
			raise ValueError, "Option type %s not supported on Galaxy" % option.type

		# We only need one item of the _short_opts and _long_opts lists
		self.short_opt = option._short_opts[0] if len(option._short_opts) > 0 else None
		self.long_opt = option._long_opts[0] if len(option._long_opts) > 0 else None

		self.label = option.help

		# If the option is boolean, by default is unselected on Galaxy (is not passed to the command)
		self.default = None
		if self.type == "boolean":
			self.default = "False"
		else:
			self.default = str(option.default) if option.default.__class__ != tuple else None

		if self.type == "select":
			self.choices = option.choices
		elif self.type == "multiple_select":
			self.choices = option.mchoices
		else:
			self.choices = None

		# Galaxy needs to know the format of the output.
		# If the output is a directory, we compress it and we pass to Galaxy the tgz file.
		self.format = None
		if self.type == "output":
			self.format = "txt"
		elif self.type == "output_dir":
			self.format = "tgz"

	def get_command_line_string(self):
		"""
			Return the command line option
		"""
		return self.short_opt if self.short_opt else self.long_opt

	def is_short_command_line(self):
		"""
			Return True if the command line option is short (e.g. '-e'),
			False if it is long (e.g. --example)
		"""
		return self.short_opt is not None

	def has_default(self):
		"""
			Return True if the option has default value
		"""
		return self.default is not None


class ScriptInfo(object):
	"""
		Class for a what an script is from Galaxy's XML point of view

		Must be given:
			- a dict of objects which it used in cogent.util.option_parsing
				to build command line interfaces according to standards developed
				in the Knight Lab, and enforced in QIIME.
				(More info at: cogent.util.option_parsing.parse_command_line_parameters)
			- the name of the script
			- the base command used to invoke the script
	"""
	def __init__(self, script_info_dict, script_name, command):
		self.id = script_name
		self.name = script_name.replace("_", " ")
		self.version = script_info_dict['version']
		self.description = script_info_dict['brief_description']
		self.required_opts = map(OptionInfo, script_info_dict['required_options'])
		try:
			self.optional_opts = map(OptionInfo, script_info_dict['optional_options'])
		except KeyError:
			self.optional_opts = []
		self.help = script_info_dict['script_description']
		self.command = command

	def _get_optional_opt(self, name):
		"""
			Returns the optional option called 'name' if it exists
		"""
		for opt in self.optional_opts:
			if opt.name == name:
				return opt
		return None

	def remove_options(self, remove_opts):
		"""
			Remove the options listed at 'remove_opts'

			Raises 'ValueError' if one of the listed options
			does not exists or it is required.
		"""
		if remove_opts:
			opt_names = remove_opts.split(',')

			for name in opt_names:
				opt = self._get_optional_opt(name)
				if opt:
					self.optional_opts.remove(opt)
				else:
					raise ValueError, "Option %s does not exists or is it a required option" % name


class CommandGenerator(object):
	"""
		Class for generate the text of the tag 'commmand'

		A ScriptInfo must be given.
	"""
	def __init__(self, info):
		self.info = info
		self.command_text = self.info.command

		self._type_dependant_functions = {}
		self._type_dependant_functions['text'] = self._generate_text_command_text
		self._type_dependant_functions['integer'] = self._generate_integer_float_command_text
		self._type_dependant_functions['float'] = self._generate_integer_float_command_text
		self._type_dependant_functions['select'] = self._generate_data_select_command_text
		self._type_dependant_functions['multiple_select'] = self._generate_data_select_command_text
		self._type_dependant_functions['data'] = self._generate_data_select_command_text
		self._type_dependant_functions['input_dir'] = self._generate_input_dir_command_text
		self._type_dependant_functions['repeat'] = self._generate_repeat_command_text
		self._type_dependant_functions['output'] = self._generate_output_command_text
		self._type_dependant_functions['output_dir'] = self._generate_output_dir_command_text
		self._type_dependant_functions['boolean'] = self._generate_boolean_command_text
		self._list_dict_to_string_is_defined = False
		self._is_optional = False
		self._uncompress_command = ""
		self._compress_command = ""

	def update(self):
		"""
			Generate the command text
		"""
		self._is_optional = False
		for option in self.info.required_opts:
			self._type_dependant_functions[option.type](option)

		self._is_optional = True
		for option in self.info.optional_opts:
			self._type_dependant_functions[option.type](option)

		self.command_text = self._uncompress_command + self.command_text + self._compress_command

	def _generate_text_command_text(self, option):
		"""
			Generate the command text for a option of type text
		"""
		option_string = " " + option.get_command_line_string()
		option_string += " " if option.is_short_command_line() else "="
		option_string += "$" + option.name

		if self._is_optional:
			option_string = "\n#if str($%s):\n%s\n#end if\n" % (option.name, option_string)

		self.command_text += option_string

	def _generate_data_select_command_text(self, option):
		"""
			Generate the command text for a option of type data or select
		"""
		option_string = " " + option.get_command_line_string()
		option_string += " " if option.is_short_command_line() else "="
		option_string += "$" + option.name

		if self._is_optional:
			option_string = "\n#if str($%s) != 'None':\n%s\n#end if\n" % (option.name, option_string)

		self.command_text += option_string

	def _generate_integer_float_command_text(self, option):
		"""
			Generate the command text for a option of type integer or float
		"""
		option_string = " " + option.get_command_line_string()
		option_string += " " if option.is_short_command_line() else "="
		option_string += "$" + option.name

		if self._is_optional:
			option_string = "\n#if $%s:\n%s\n#end if\n" % (option.name, option_string)

		self.command_text += option_string

	def _generate_boolean_command_text(self, option):
		"""
			Generate the command text for a option of type boolean
		"""
		self.command_text += "\n#if $%s:\n %s\n#end if\n" % (option.name, option.get_command_line_string())

	def _generate_repeat_command_text(self, option):
		"""
			Generate the command text for a option of type repeat
		"""
		option_string = ""

		if not self._list_dict_to_string_is_defined:
			option_string += LIST_DICT_TO_STRING_FUNCTION
			self._list_dict_to_string_is_defined = True

		option_string += " " + option.get_command_line_string()
		option_string += " " if option.is_short_command_line() else "="
		option_string += "$list_dict_to_string($input_files_%s)" % option.name

		if self._is_optional:
			option_string = "\n#if $input_files_%s:\n%s\n#end if\n" % (option.name, option_string)

		self.command_text += option_string

	def _generate_output_command_text(self, option):
		"""
			Generate the command text for a option of type output
		"""
		option_string = " " + option.get_command_line_string()
		option_string += " " if option.is_short_command_line() else "="
		option_string += "$" + option.name
		
		self.command_text += option_string

	def _generate_output_dir_command_text(self, option):
		"""
			Generate the command text for a option of type output_dir
		"""
		if self._compress_command != "":
			raise ValueError, "Two options which generate a directory as output is not allowed!"

		output_dir = self.info.id + "_output"

		option_string = " " + option.get_command_line_string()
		option_string += " " if option.is_short_command_line() else "="
		option_string += output_dir

		self._compress_command = COMMAND_LINE_COMPRESS % (output_dir, option.name)

		self.command_text += option_string

	def _generate_input_dir_command_text(self, option):
		"""
			Generate the command text for a option of type input_dir
		"""
		if self._uncompress_command != "":
			raise ValueError, "Two options which generate a directory as input is not allowed!"

		input_dir = self.info.id + "_input"

		option_string = " " + option.get_command_line_string()
		option_string += " " if option.is_short_command_line() else "="
		option_string += input_dir

		self._uncompress_command = COMMAND_LINE_UNCOMPRESS % (option.name, input_dir)

		self.command_text += option_string


class XmlOptionsAttributesGenerator(object):
	"""
		Class for generate the XML tags and attributes of the inputs and the outputs

		Must be given:
			- a ScriptInfo
			- a xml.dom.minidom.Document
			- inputs node of the XML document
			- outputs node of the XML document
	"""
	def __init__(self, info, doc, inputs, outputs):
		self.info = info
		self.doc = doc
		self.inputs = inputs
		self.outputs = outputs

		self._is_optional = False

		self._type_dependant_functions = {}
		self._type_dependant_functions['text'] = self._generate_text_data_attributes
		self._type_dependant_functions['integer'] = self._generate_integer_float_attributes
		self._type_dependant_functions['float'] = self._generate_integer_float_attributes
		self._type_dependant_functions['select'] = self._generate_select_attributes
		self._type_dependant_functions['multiple_select'] = self._generate_multiple_select_attributes
		self._type_dependant_functions['data'] = self._generate_text_data_attributes
		self._type_dependant_functions['input_dir'] = self._generate_input_dir_attributes
		self._type_dependant_functions['repeat'] = self._generate_repeat_attributes
		self._type_dependant_functions['output'] = self._generate_output_attributes
		self._type_dependant_functions['output_dir'] = self._generate_output_attributes
		self._type_dependant_functions['boolean'] = self._generate_boolean_attributes

	def update(self):
		"""
			Updates the inputs and outputs node adding the script options
		"""
		self._is_optional = False
		for option in self.info.required_opts:
			self._type_dependant_functions[option.type](option)

		self._is_optional = True
		for option in self.info.optional_opts:
			self._type_dependant_functions[option.type](option)

	def _generate_integer_float_attributes(self, option):
		"""
			Generate the XML nodes and attributes for a option of type integer.
		"""
		param = self.doc.createElement("param")
		param.setAttribute("name", option.name)
		param.setAttribute("type", option.type)
		param.setAttribute("label", option.label.replace("%default", str(option.default)))
		param.setAttribute("optional", str(self._is_optional))

		if option.has_default():
			param.setAttribute("default", option.default)
		if not self._is_optional:
			param.setAttribute("value", "0")

		self.inputs.appendChild(param)


	def _generate_text_data_attributes(self, option):
		"""
			Generate the XML nodes and attributes for a option of type text,
			float and data.
		"""
		param = self.doc.createElement("param")
		param.setAttribute("name", option.name)
		param.setAttribute("type", option.type)
		param.setAttribute("label", option.label.replace("%default", str(option.default)))
		param.setAttribute("optional", str(self._is_optional))

		if option.has_default():
			param.setAttribute("default", option.default)

		self.inputs.appendChild(param)

	def _generate_input_dir_attributes(self, option):
		"""
			Generate the XML nodes and attributes for a option of type input_dir
		"""
		param = self.doc.createElement("param")
		param.setAttribute("name", option.name)
		param.setAttribute("type", "data")
		param.setAttribute("label", option.label.replace("%default", str(option.default)))

		self.inputs.appendChild(param)

	def _generate_select_attributes(self, option):
		"""
			Generate the XML nodes and attributes for a option of type select
		"""
		param = self.doc.createElement("param")
		param.setAttribute("name", option.name)
		param.setAttribute("type", option.type)
		param.setAttribute("label", option.label.replace("%default", str(option.default)))

		if self._is_optional:
			opt = self.doc.createElement("option")
			opt.setAttribute("value", "None")
			opt.setAttribute("selected", "True")
			opt_text = self.doc.createTextNode("Selection is Optional")
			opt.appendChild(opt_text)
			param.appendChild(opt)

		for choice in option.choices:
			opt = self.doc.createElement("option")
			opt.setAttribute("value", choice)
			opt_text = self.doc.createTextNode(choice)
			opt.appendChild(opt_text)
			param.appendChild(opt)

		param.setAttribute("optional", str(self._is_optional))
		self.inputs.appendChild(param)

	def _generate_multiple_select_attributes(self, option):
		"""
			Generate the XML nodes and attributes for a option of type select
		"""
		param = self.doc.createElement("param")
		param.setAttribute("name", option.name)
		param.setAttribute("type", "select")
		param.setAttribute("label", option.label.replace("%default", str(option.default)))
		param.setAttribute("multiple", "True")

		if self._is_optional:
			opt = self.doc.createElement("option")
			opt.setAttribute("value", "None")
			opt.setAttribute("selected", "True")
			opt_text = self.doc.createTextNode("Selection is Optional")
			opt.appendChild(opt_text)
			param.appendChild(opt)

		for choice in option.choices:
			opt = self.doc.createElement("option")
			opt.setAttribute("value", choice)
			opt_text = self.doc.createTextNode(choice)
			opt.appendChild(opt_text)
			param.appendChild(opt)

		param.setAttribute("optional", str(self._is_optional))
		self.inputs.appendChild(param)

	def _generate_repeat_attributes(self, option):
		"""
			Generate the XML nodes and attributes for a option of type repeat
		"""
		repeat = self.doc.createElement("repeat")
		repeat.setAttribute("name", "input_files_%s" % option.name)
		repeat.setAttribute("title", option.name)
		repeat.setAttribute("optional", str(self._is_optional))

		param = self.doc.createElement("param")
		param.setAttribute("name", "additional_input")
		param.setAttribute("type", "data")
		param.setAttribute("label", option.label.replace("%default", str(option.default)))

		repeat.appendChild(param)
		self.inputs.appendChild(repeat)
		
	def _generate_output_attributes(self, option):
		"""
			Generate the XML nodes and attributes for a option of type output
		"""
		data = self.doc.createElement("data")
		data.setAttribute("name", option.name)
		data.setAttribute("format", option.format)
		self.outputs.appendChild(data)

	def _generate_boolean_attributes(self, option):
		"""
			Generate the XML nodes and attributes for a option of type boolean
		"""
		param = self.doc.createElement("param")
		param.setAttribute("type", option.type)
		param.setAttribute("name", option.name)
		param.setAttribute("label", option.label.replace("%default", str(option.default)))
		param.setAttribute("selected", option.default)
		self.inputs.appendChild(param)

def generate_xml_string(info):
	"""
		Generate the xml string
	"""
	doc = Document()

	# Setting tool attributes
	tool = doc.createElement("tool")
	tool.setAttribute("id", info.id)
	tool.setAttribute("name", info.name)
	tool.setAttribute("version", info.version)
	doc.appendChild(tool)

	# Setting description attributes
	description = doc.createElement("description")
	descr_text = doc.createTextNode(info.description)
	description.appendChild(descr_text)
	tool.appendChild(description)

	# Setting requirements attributes
	requirements = doc.createElement("requirements")
	req = doc.createElement("requirement")
	req.setAttribute("type", "package")
	req_text = doc.createTextNode("qiime")
	req.appendChild(req_text)
	requirements.appendChild(req)
	tool.appendChild(requirements)

	# Setting command attributes
	command = doc.createElement("command")
	command_generator = CommandGenerator(info)
	command_generator.update()
	command_text = doc.createTextNode(command_generator.command_text)
	command.appendChild(command_text)
	tool.appendChild(command)

	# Setting inputs and outputs attributes
	inputs = doc.createElement("inputs")
	outputs = doc.createElement("outputs")
	xml_options_generator = XmlOptionsAttributesGenerator(info, doc, inputs, outputs)
	xml_options_generator.update()
	tool.appendChild(inputs)
	tool.appendChild(outputs)

	# Setting help attributes
	help = doc.createElement("help")
	help_text = doc.createTextNode(info.help)
	help.appendChild(help_text)
	tool.appendChild(help)

	return doc.toprettyxml(indent="\t")

def make_xml(script_fp, output_dir, remove_opts):
	"""
		Generate the xml file
	"""
	dir_path, command = split(script_fp)
	fname, ext = splitext(command)

	script = __import__(fname)

	# Create the script info
	info = ScriptInfo(script.script_info, fname, command)

	# Remove the options that the user does not want to appear in the XML
	info.remove_options(remove_opts)

	# Get the xml string
	string_xml = generate_xml_string(info)

	# Create the xml file
	outf = open(join(output_dir, fname+".xml"), 'w')
	outf.write(string_xml)
	outf.close()
