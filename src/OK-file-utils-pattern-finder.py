"""OK-file-utils collection: PATTERN finder

OK-file-utils is a collection of scripts for manipulation and analyze 
generic files and documents.

This script search a defined pattern inside the files of a desired
folder, or comparing two folders.
The pattern and the desired file extension are defined by regex.

The results is showed on console or saved into text file "report.txt".

For usage information please run:
$ python OK-file-utils-pattern-finder.py --help
"""

# Created by: lisr-pcx (https://github.com/lisr-pcx/OK-file-utils)
# This is free software and it comes with absolutely no warranty.

import os
import argparse
import re
from datetime import datetime

# Regex to process only files with specific extension
# USER CAN CHANGE IT ACCORDING TO NEEDS!
re_file_ext = r'^.*\.(ads|adb|c|h|cpp|hpp|txt)$'

# Regex of the pattern to search inside the files
# USER CAN CHANGE IT ACCORDING TO NEEDS!
re_PATTERN_format = r'(atvcm[0-9]+){1,}'

# Store found patterns in a key-value data structure where
#     key: is a string which identify the file fullpath
#     value: is a set() that contains all patterns found
result_directory_A = dict()
result_directory_B = dict()

# Store the results into a list of string.
# These info are written into file "report.txt".
report_info = []

# Use specific colors in terminal formatted output
class TerminalColors:
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'

def search_pattern_into_file(filepath: str):
    """Read the file line by line looking for the pattern.

    Parameters
    ----------
    filepath : str
               full path of the file
    
    Returns
    -------
    items : set
              unique list of matching elements
    """

    items = []
    if os.path.isfile(filepath):
        # Analyze line by line

        # TODO: improve read/open of file format (unicode, ascii ...)
        # pyhton3 manages in a different way than python2, there are
        # few articles online about it...
        # Please make the open file below compatible and fault tolerant.
        # Previous code was:
        #     with open(filepath, 'r', encoding="utf-8") as f:

        try:
            with open(filepath, 'r', encoding="latin-1") as f:            
                for line in f:                
                    # Work line by line adding results to tmp_list variable
                    tmp_list = re.findall(re_PATTERN_format, line, re.IGNORECASE)
                    if len(tmp_list) > 0:
                        items.extend(tmp.lower() for tmp in tmp_list)
        except Exception as e:
            print(f"{TerminalColors.FAIL}ERR: {str(e)} (!) Skip file {TerminalColors.END}")
    else:
        print("File not found! [" + filepath + "]")
    return set(items)

def walk_dir_recursively(rootdirpath: str):
    """Starting from root path it walks directories recursively 
    looking for the pattern.

    Parameters
    ----------
    rootdirpath : str
                  directory where to start the search
    
    Returns
    -------
    result_for_dir : dict
                     key-value structure listing for each path (key) the 
                     found elements
    """
    
    result_for_dir = dict()
    for tmp_path, tmp_dirs, tmp_files in os.walk(rootdirpath):        
        for target_file in tmp_files:
            # Look into all files inside the folder            
            file_is_valid = re.search(re_file_ext, str(target_file))
            # Only files matching the desired extension are used during search
            if file_is_valid:
                file_fullpath = str(tmp_path) + "\\" + str(target_file)
                element_founds = search_pattern_into_file(file_fullpath)

                if len(element_founds)>0:
                    # Debug
                    if arguments_list.verbose:
                        print(f"{TerminalColors.OKGREEN}file {str(file_fullpath)}{TerminalColors.END}")                    
                        print(f"{TerminalColors.OKGREEN}found {str(len(element_founds))} items: {str(element_founds)}{TerminalColors.END}")
                    # Store results
                    if target_file in result_for_dir.keys():
                        result_for_dir[file_fullpath.replace(rootdirpath, '')] = result_for_dir[target_file].union(element_founds)
                    else:
                        result_for_dir[file_fullpath.replace(rootdirpath, '')] = element_founds
    return result_for_dir

def update_report_info(filepath: str, 
                       items_A=[], 
                       items_BOTH=[], 
                       items_B=[], 
                       show_compare_dir=False):
    """Store the results into report_info data structure according to user args.

    Parameters
    ----------
    filepath : str
               full path
    items_A : list
              these elements have been found only inside the first folder
    items_BOTH : list
                 these elements have been found on both folders
    items_A : list
              these elements have been found only inside the second folder
    """

    global report_info
    if show_compare_dir == False:
        # Only single directory
        print(f"\n{TerminalColors.OKGREEN}{filepath}:{TerminalColors.END}")
        print(f"  |-- found : {str(items_A)}")
        report_info.append(filepath + "\n")
        report_info.append("  |-- found : " + str(items_A) + "\n\n")   

    elif arguments_list.diff:
        # Exclude common elements
        if len(items_A)>0 or len(items_B)>0:
            print(f"\n{TerminalColors.OKGREEN}{filepath}:{TerminalColors.END}")
            print(f"  |-- only A : {str(items_A)}")
            print(f"  |-- only B : {str(items_B)}")            
            # Update information for output file
            report_info.append(filepath + "\n")
            report_info.append("  |-- only A : " + str(items_A)    + "\n")            
            report_info.append("  |-- only B : " + str(items_B)    + "\n\n")

    else:
        # Incude common elements    
        if len(items_A)>0 or len(items_BOTH)>0 or len(items_B)>0:
            print(f"\n{TerminalColors.OKGREEN}{filepath}:{TerminalColors.END}")
            print(f"  |-- only A : {str(items_A)}")
            print(f"  |-- BOTH   : {str(items_BOTH)}")
            print(f"  |-- only B : {str(items_B)}")        
            # Update information for output file
            report_info.append(filepath + "\n")
            report_info.append("  |-- only A : " + str(items_A)    + "\n")
            report_info.append("  |-- BOTH   : " + str(items_BOTH) + "\n")
            report_info.append("  |-- only B : " + str(items_B)    + "\n\n")

def write_report_info():
    """write results into file: report.txt"""

    global report_info
    output_file = open("report.txt", "w")
    output_file.write("SCRIPT: OK-file-utils-pattern-finder.py\n")
    output_file.write("REPORT on: " + str(datetime.now()) + "\n\n")
    output_file.write("Directory A: " + str(arguments_list.dirpath_A) + "\n")
    output_file.write("Directory B: " + str(arguments_list.dirpath_B) + "\n\n")
    for l in report_info:
        output_file.write(l)
    output_file.close()

def create_arg_parser():
    """Creates and returns the ArgumentParser object"""

    parser = argparse.ArgumentParser(
                        prog='python.exe OK-file-utils-pattern-finder.py',
                        description='Search a pattern into files from single or two desired folders.',
                        epilog='This is free software and it comes with absolutely no warranty.')
    parser.add_argument('dirpath_A',
                        type=str,
                        help='First folder to search (A)')
    parser.add_argument("dirpath_B",
                        nargs="?",
                        default="",
                        type=str,
                        help='Second folder to search (B)')
    parser.add_argument('-o', '--output',
                        action='store_true',
                        help='Store results into file report.txt (default is false).')
    parser.add_argument('-d', '--diff',
                        action='store_true',
                        help='Show only different items between the two folders (default is false).')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='Show detailed logging (default is false).')
    return parser

if __name__ == "__main__":
    arguments = create_arg_parser()
    arguments_list = arguments.parse_args()    
    
    print(f"{TerminalColors.OKBLUE}Look in folder: {arguments_list.dirpath_A} {TerminalColors.END}")
    print(f"{TerminalColors.OKBLUE}Search pattern ...{TerminalColors.END}")
    result_directory_A = walk_dir_recursively(arguments_list.dirpath_A)

    report_info.clear()
    if not arguments_list.dirpath_B:
        # Show only results about first folder
        print(f"\n{TerminalColors.OKBLUE}Single DIR results:{TerminalColors.END}")    
        for k in result_directory_A.keys():
            update_report_info(k, list(result_directory_A[k]))
    else:        
        print(f"{TerminalColors.OKBLUE}Look in folder: {arguments_list.dirpath_B} {TerminalColors.END}")
        print(f"{TerminalColors.OKBLUE}Search pattern ...{TerminalColors.END}")
        result_directory_B = walk_dir_recursively(arguments_list.dirpath_B)

        # Show results for both folders
        # (Please note that compare files with the same relative path)
        print(f"\n{TerminalColors.OKBLUE}Compare of DIRs result:{TerminalColors.END}")
        for k in result_directory_A.keys() & result_directory_B.keys():
            dir_A = result_directory_A[k]
            dir_B = result_directory_B[k]
            only_A = dir_A.difference(dir_B)
            both_AB = dir_A & dir_B
            only_B = dir_B.difference(dir_A)
            # Convert set() to list for better prints
            update_report_info(k, list(only_A), list(both_AB), list(only_B), True)
    
    # Store information into file
    if arguments_list.output:
        write_report_info()

    print(f"{TerminalColors.OKBLUE}End{TerminalColors.END}\n")
