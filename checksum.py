'''
Purpose: To create and match checksum for files at the source and destination folder respectively.
For help and usage: checksum.py --help
'''

# Import Standard Library
import hashlib
import os
import json
from optparse import OptionParser
import argparse
import argparse
from datetime import datetime


# Functions
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Main
if __name__ == "__main__":
    startTime = datetime.now()
    
    # Commanline argument parser.
    parser = argparse.ArgumentParser()

    # Positional arguments.
    parser.add_argument("mode", help="create or match checksum at the source or destination respectively", choices=['create', 'match'])
    parser.add_argument("path", help="source or destination directory path")

    # Fetch arguments.
    args = parser.parse_args()
    dir_path = args.path
    mode = args.mode
    
    # Execute checksum creation of matching depending upon the mode selected.
    if mode == 'create':
        
        output_file = os.path.join(dir_path,"md5_hash_at_source.json")
        print("In create mode.\nAre you sure you are at the source? Proceeding further will delete any old {} output file and create a new one.".format(output_file))
        proceed = input("To proceed enter [y/n]:")

        if proceed == "y":
            if os.path.isfile(output_file):
                print("Deleting old {}".format(output_file))
                os.remove(output_file)

            # List files names, ignoring files starting with a dot.
            files_list = sorted([f for f in os.listdir(dir_path) if not f.startswith('.')])
            total_no_files = len(files_list)
            count = 0

            # Calculate MD5 hash per file and write the dictionary with the results in a json file.
            file_hash = {}
            for i  in files_list:
                count += 1
                print("\rCalculating checksum for: {}/{} files.".format(count, total_no_files), end="")
                path_plus_file = os.path.join(dir_path,i)
                hash_md5 = md5(path_plus_file)
                file_hash[i] = hash_md5
            print("\nSaving results in {} \nDone in {} seconds. \n".format(output_file, datetime.now() - startTime))
            with open(output_file, 'w') as file:
                json.dump(file_hash, file)

        elif proceed == "n":
            exit()
    
    elif mode == 'match':

        # Load the pre-calculated MD5 hash at the source and re-calculate
        # MD5 hash at the destination and compare them with the source.
        input_file = os.path.join(dir_path,"md5_hash_at_source.json")
        print("In match mode.\nLoading {}".format(input_file))
        try:
            with open(input_file) as file:
                source_file_hash = json.load(file)
        except FileNotFoundError:
            print("Error: {} not found at the destination. Are you sure you calculated the checksum at the source?".format(input_file))
            exit()
        total_no_files = len(source_file_hash)
        matched = 0
        unmatched = 0
        unmatched_files = []
        count = 0
        for key, value in source_file_hash.items():
            count += 1
            print("\rCalculating and matching checksum for: {}/{} files.".format(count, total_no_files), end="")
            hash_md5 = md5(os.path.join(dir_path, key))
            if hash_md5 == value:
                matched += 1
            else:
                unmatched += 1
                unmatched_files.append(key)
        
        # Report checksum matching stats on the console.
        print("\r")
        print("Checksum matched for {}/{}".format(matched, total_no_files))
        print("Checksum failed for {}/{}".format(unmatched, total_no_files))
        print("\rDone in {} seconds. \n".format(datetime.now() - startTime))
        if unmatched > 0:
            print("List of file(s) with a failed checksum.")
            print("---------------------------------------")
            print(*unmatched_files, sep='\n')
            print("\n")
