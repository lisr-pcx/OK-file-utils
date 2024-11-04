# OK-file-utils

**O**verrated **K**it file utils is a collection of scripts for manipulation and analysis of files and documents.

For a list of available features please refer to **Usage** section.

## Installation

Make sure to have Python installed. All scripts have been developed using *Python 3.11.10*.

## Usage example

Please refer to specific **help** of the scripts:

```sh
python3 OK_file_SCRIPTNAME.py --help
python3 OK_file_SCRIPTNAME.py -h
```

### OK-file-utils-cr-finder.py

List the occurence of a pattern (i.e. Change Request codes) from select files inside a directory.  

To search inside a directory:

```sh
python3 OK_file_utils_pattern_finder.py YOURFOLDER
```

To search and compare between two directories:

```sh
python3 OK_file_utils_pattern_finder.py YOURFIRSTFOLDER YOURSECONDFOLDER
```

Adding `-o` or `--ouput` will store the result in a file named *report.txt*:

```sh
python3 OK_file_utils_pattern_finder.py YOURFIRSTFOLDER YOURSECONDFOLDER --output
```

The pattern and the extension of the files are defined by regex, and they can be customized inside the script.  
In the example below it look for files "*.c", "*.h", "*.txt" that contain text with an identification codes for change request like atvcm1201, atvcm1202 ...

```python
re_file_ext = r'^.*\.(c|h|txt)$'
re_CR_format = r'(atvcm[0-9]+){1,}'
```

## Meta

Created by: lisr-pcx [https://github.com/lisr-pcx/OK-file-utils](https://github.com/lisr-pcx/OK-file-utils)

Distributed under the UN-license. See file ``LICENSE`` for more information.

## Links and references

[The Python Language Reference](https://docs.python.org/3/reference/index.html)

Unit testing:

[Unittest documentation](https://docs.python.org/3/library/unittest.html)  
[How to write unit tests](https://www.freecodecamp.org/news/how-to-write-unit-tests-for-python-functions/)

How to write documentation:

[Documenting Python Code: A Complete Guide](https://realpython.com/documenting-python-code/)  
[PEP 257 – Docstring Conventions](https://peps.python.org/pep-0257/)  
[How to write a great README for your GitHub project](https://dbader.org/blog/write-a-great-readme-for-your-github-project)  
[Numpy doc style guide](https://numpydoc.readthedocs.io/en/latest/format.html)  
