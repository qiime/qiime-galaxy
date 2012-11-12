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
from shutil import rmtree, copyfile
from os import mkdir, path, remove
from tgz_manager import compress_to_tgz, extract_from_tgz, ERROR_MSG
from cogent.app.util import get_tmp_filename
import tempfile

class TgzManagerTest(TestCase):
	def setUp(self):
		self.tmp_dir = tempfile.gettempdir()

		self.tgz_dir = './support_files/tar_dir.tgz'
		self.tgz_file = './support_files/tar_file.tgz'

		self.tgz_dir_file1 = 'file1.txt'
		self.tgz_dir_file2 = 'file2.txt'
		self.tgz_dir_file3 = 'file3.txt'

		self._paths_to_clean_up = []
		self._dirs_to_clean_up = []

	def tearDown(self):
		map(remove, self._paths_to_clean_up)
		map(rmtree, self._dirs_to_clean_up)

	def test_compress_to_tgz(self):
		#test compressing a single file
		filename = get_tmp_filename(tmp_dir=self.tmp_dir)
		f = open(filename, 'w')
		f.close()

		output_tgz = get_tmp_filename(tmp_dir=self.tmp_dir, suffix='.tgz')

		self._paths_to_clean_up = [filename, output_tgz]

		compress_to_tgz(filename, output_tgz)
		self.assertTrue(path.exists(output_tgz), 'The tgz file was not created in the appropiate location')

		#test compressing a directory
		dirname = get_tmp_filename(tmp_dir=self.tmp_dir)
		mkdir(dirname)
		fileA = get_tmp_filename(tmp_dir=dirname)
		f = open(fileA, 'w')
		f.close()
		fileB = get_tmp_filename(tmp_dir=dirname)
		f = open(fileB, 'w')
		f.close()

		output_tgz = get_tmp_filename(tmp_dir=self.tmp_dir, suffix='.tgz')
		
		self._paths_to_clean_up.append(output_tgz)
		self._dirs_to_clean_up = [dirname]

		compress_to_tgz(dirname, output_tgz)
		self.assertTrue(path.exists(output_tgz), 'The tgz file was not created in the appropiate location')


	def test_extract_from_tgz(self):
		#test with a tgz file which contains only one file
		filename = get_tmp_filename(tmp_dir=self.tmp_dir)
		copyfile(self.tgz_file, filename)

		path_name = get_tmp_filename(tmp_dir=self.tmp_dir)

		self._paths_to_clean_up = [filename, path_name]

		extract_from_tgz(filename, path_name)
		self.assertTrue(path.exists(path_name), 'The output file was not created in the appropiate location')
		self.assertTrue(path.isfile(path_name), 'The output was not a file')

		#test with a tgz file which contains multiple files
		filename = get_tmp_filename(tmp_dir=self.tmp_dir)
		copyfile(self.tgz_dir, filename)

		path_name = get_tmp_filename(tmp_dir=self.tmp_dir)

		self._paths_to_clean_up.append(filename)
		self._dirs_to_clean_up = [path_name]

		extract_from_tgz(filename, path_name)

		self.assertTrue(path.exists(path_name), 'The output directory was not created in the appropiate location')
		self.assertTrue(path.isdir(path_name), 'The output was not a directory')
		self.assertTrue(path.exists(path.join(path_name, self.tgz_dir_file1)), 'The tgz contents were not extracted correctly')
		self.assertTrue(path.exists(path.join(path_name, self.tgz_dir_file2)), 'The tgz contents were not extracted correctly')
		self.assertTrue(path.exists(path.join(path_name, self.tgz_dir_file3)), 'The tgz contents were not extracted correctly')

		#test passing a file which is not a tgz
		filename = get_tmp_filename(tmp_dir=self.tmp_dir)
		f = open(filename, 'w')
		f.write("A")
		f.close()

		self._paths_to_clean_up.append(filename)

		self.assertRaises(ValueError, extract_from_tgz, filename, "")

if __name__ == '__main__':
	main()