#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The Galaxy-QIIME Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from os import path, mkdir, walk, remove
from shutil import copyfile
from site import addsitedir
from xml.dom.minidom import parse, Document
from xml_generator import make_xml

def parse_config_file(lines):
    """Parser for the Galaxy-QIIME configuration file

    Returns:
        result: a dict of {script:(section, remove_opts)}
        sections: list with all sections

    Note: raises a ValueError if the format of the configuration file is not
        correct
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
    """Create directories in the galaxy tool folder for all the QIIME sections

    Inputs:
        galaxy_dir: the full path to the Galaxy installation directory
        sections: a list with the different sections in which the QIIME scripts
            will be grouped by

    Note: raises a ValueError if the galaxy_dir path doesn't follow the
        directory structure of a Galaxy installation directory
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
    """Generates the contents of the Galaxy's tool_conf.xml file

    Inputs:
        galaxy_dir: the full path to the Galaxy installation directory
        update: boolean showing if the current tool_conf file should be updated
            or a new tool_conf file should be created

    Returns a xml.dom.minidom.Document object which contains the tool_conf.xml
    file. If update is True, it parses the current tool_conf.xml file present
    in the Galaxy installation folder and updates it. Otherwise, it generates
    a new tool_conf.xml file from scratch.

    Note: raises a ValueError if the galaxy_dir path doesn't follow the
        directory structure of a Galaxy installation directory
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
    """Returns the XML node that corresponds to the provided section

    Inputs:
        section: string containing the name of the section to be searched
        xml: the xml.dom.minidom.Document object where the search should be
            performed

    Searches in the xml.dom.minidom.Document 'xml' for the section node that
    corresponds to the section 'section'. If it doesn't exists, returns None.
    """
    for node in xml.getElementsByTagName('section'):
        if node.attributes.getNamedItem('name').value == section:
            return node
    return None

def exist_script_in_section(script, section_node):
    """Checks if the script exists in the given XML section node

    Inputs:
        script: string containing the name of the script to be searched
        section_node: DOM Element object of a section where the search should
            be performed

    Returns True if the script 'script' is present in the XML section node
    'section_node'. Otherwise, returns False.
    """
    name, ext = path.splitext(script)
    filepath = section_node.attributes.getNamedItem('name').value.replace(" ",
        "").lower() + "/" + name + ".xml"

    for node in section_node.childNodes:
        if node.attributes != None and \
            node.attributes.getNamedItem('file').value == filepath:
            return True
    return False

def add_section_to_xml(section, script_list, xml):
    """Adds the specified section with the given scripts to the XML document

    Inputs:
        section: string with the name of the section to be added
        script_list: a list with the scripts names to be added under the new
            section
        xml: the xml.dom.minidom.Document object where to add the new section
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
    """Updates the tool_conf xml file with the specified sections

    Inputs:
        tool_conf: the xml.dom.minidom.Document object to be updated with the
            new sections and scripts indicated by section_dict
        section_dict: a dictionary of {'section name': scripts_list}

    It modifies the tool_conf xml.dom.minidom.Document in order to contain also
    the information of section_dict
    """
    for section in section_dict.keys():
        section_node = get_section_node(section, tool_conf)
        if section_node:
            for script in section_dict[section]:
                if not exist_script_in_section(script, section_node):
                    name, ext = path.splitext(script)
                    filepath = section.replace(" ", "").lower()\
                        + "/" + name + ".xml"
                    tool_node = tool_conf.createElement('tool')
                    tool.setAttribute("file", filepath)
                    section_node.appendChild(tool_node)
        else:
            add_section_to_xml(section, section_dict[section], tool_conf)

def create_activate_file(galaxy_dir):
    """Generates the activate.sh file in the Galaxy installation folder

    Input:
        galaxy_dir: the full path to the Galaxy installation directory

    The activate.sh contains the environment variables definitions needed
    for running QIIME within the Galaxy environment
    """
    activate_fp = path.join(galaxy_dir, 'activate.sh')
    if path.exists(activate_fp):
        activate_bak_fp = path.join(galaxy_dir, 'activate.sh.bak')
        copyfile(activate_fp, activate_bak_fp)
        remove(activate_fp)
    f = open(activate_fp, 'w')
    f.write("export GALAXY_HOME=%s\n" % galaxy_dir)
    f.close()

def integrate(scripts_dir, galaxy_dist_dir, config_file, update_tool_conf,
                                                                        log_fp):
    """Integrates the tools in the scripts folder into the given Galaxy instance

    Inputs:
        scripts_dir: path to the directory containing all the scripts to be 
            integrated on Galaxy
        galaxy_dist_dir: path to the Galaxy's installation folder
        config_file: path to the Galaxy-QIIME configuration file
        update_tool_conf: boolean showing if the current tool_conf file should
            be updated or a new tool_conf file should be created 
        log_fp: path to where the log file should be written

    Walks through all the scripts present in the 'scripts_dir' folder and 
    integrates them in the Galaxy instance 'galaxy_dist_dir'. The integration is
    done according to the 'config_file', which specifies: the different sections
    in which the scripts will be grouped, which scripts of the script folder 
    will be integrated and which option of these script will NOT be included
    in the Galaxy interface.

    If update_tool_conf is True, it will update the current tool_conf.xml file
    present in the Galaxy instance. Otherwise, it will override it with a new
    tool_conf.xml configuration file.

    If a log_fp is given, the script will write the log file into this path.
    Otherwise, it will create a log file in the scripts_dir folder
    """
    script_dict, sections = parse_config_file(open(config_file, 'U'))

    galaxy_dist_dir = path.abspath(galaxy_dist_dir)

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
                    output_dir = path.join(galaxy_dist_dir, 'tools',
                        section.replace(" ", "").lower())
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

    log_file.write("Generating activate.sh file... ")
    create_activate_file(galaxy_dist_dir)
    log_file.write("Ok\n")

    # Close log file
    log_file.close()