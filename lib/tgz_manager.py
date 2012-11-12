#!/usr/bin/env python

__author__ = "Jose Antonio Navas"
__copyright__ = "Copyright 2011, The QIIME Project"
__credits__ = ["Jose Antonio Navas"]
__license__ = "GPL"
__version__ = "1.4.0-dev"
__maintainer__ = "Jose Antonio Navas"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

import tarfile
from shutil import move
from os import path

ERROR_MSG = "'tgz_file' is not a gzip file!"

def compress_to_tgz(in_path, tgz_name):
	"""
		in_path: path to compress
		tgz_name: name of the .tgz file

		generates a .tgz file which contains the 'in_path' tree with name tgz_name
	"""
	t = tarfile.open(name = tgz_name, mode = 'w:gz')
	t.add(in_path, path.basename(in_path))
	t.close()

def extract_from_tgz(tgz_file, output_path):
	"""
		tgz_file: filepath to .tgz file
		output_path: path name of the output

		extract the contents of tgz_file in a directory named 'output_path'.
		If the tgz_file only contains one file, then is extracted in the
		current directory an renamed as 'output_path'

		Raises a ValueError if tgz_file is not a tgz_file
	"""
	try:
		t = tarfile.open(name = tgz_file, mode = 'r:gz')
		names_list = t.getnames()
		#if the tgz_file only has one file is not necessary to generate an output directory
		if len(names_list) == 1:
			t.extractall()
			move(names_list[0], output_path)
		else:
			t.extractall(path=output_path)
		t.close()
	except tarfile.ReadError, e:
			if str(e) == "not a gzip file":
				raise ValueError, ERROR_MSG
			raise tarfile.ReadError, e