#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The Galaxy-QIIME Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from cogent.util.unit_test import TestCase, main
from shutil import copyfile, copytree, rmtree
from os import path, remove
from cogent.app.util import get_tmp_filename
import tempfile
from format_blast_db_string import format_blast_db_string

class FormatBlastDBStringTest(TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.gettempdir()

        test_dir = path.dirname(path.abspath(__file__))

        self.refseqs_fp = path.join(test_dir, './support_files/refseqs.fasta')
        self.blast_db_dirpath = path.join(test_dir, './support_files/blast_db')

        self._paths_to_clean_up = []
        self._dirs_to_clean_up = []

    def tearDown(self):
        map(remove, self._paths_to_clean_up)
        map(rmtree, self._dirs_to_clean_up)

    def test_format_blast_db_string_file(self):
        """Test when path is fasta file"""
        filename = get_tmp_filename(tmp_dir=self.tmp_dir)
        copyfile(self.refseqs_fp, filename)

        self._paths_to_clean_up = [filename]

        obs = format_blast_db_string(filename)
        self.assertEqual(obs, filename)

    def test_format_blast_db_string_dir(self):
        """Test when path is a blast db base directory"""
        dirname = get_tmp_filename(tmp_dir=self.tmp_dir, suffix='')
        copytree(self.blast_db_dirpath, dirname)

        self._dirs_to_clean_up = [dirname]

        obs = format_blast_db_string(dirname)
        exp = path.join(dirname, 'refseqs.fasta')
        self.assertEqual(obs, exp)

if __name__ == '__main__':
    main()