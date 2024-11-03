# Unit test for project: OK-file-utils-pattern-finder.py

# Created by: lisr-pcx (https://github.com/lisr-pcx/OK-file-utils)
# This is free software and it comes with absolutely no warranty.

# Add current project to system path
import sys
from pathlib import Path
project_root_path = Path(__file__).parents[1]
sys.path.append(str(project_root_path))

import os
import unittest
from src.OK_file_utils_pattern_finder import search_pattern_into_file

class TestClass(unittest.TestCase):

	def setUp(self):
		# create file ad hoc for test purpose
		self.samplefilepath = 'sample.txt'
		f = open(self.samplefilepath, 'w')
		f.write("Sample text file automatically created when running test cases\n")
		f.write("atvcm\n")
		f.write("atvcmATVCM\n")
		f.write("atvcm0\n")
		f.write("atvcm1\n")
		f.write("ATVCM2\n")
		f.write("atvcm0123456789\n")
		f.write("atvcm23498\n")
		f.write("atv234cm234\n")
		f.write("678atvcm\n")
		f.write("atvcm 223344\n")
		f.close()

	def test_n_of_match(self):
		output = search_pattern_into_file(self.samplefilepath)
		# Debug
		# print(TestClass.test_n_of_match.__name__ + " - Match found: " + str(len(output)))
		self.assertTrue(len(output) == 5)

	def test_list_of_match(self):
		valid = {'atvcm2', 'atvcm23498', 'atvcm0123456789', 'atvcm1', 'atvcm0'}
		output = search_pattern_into_file(self.samplefilepath)
		# Debug
		# print(TestClass.test_n_of_match.__name__ + " - Match found: " + str(output))
		self.assertEqual(valid, output)

	def tearDown(self):
		os.remove(self.samplefilepath)

if __name__ == '__main__':
	unittest.main()