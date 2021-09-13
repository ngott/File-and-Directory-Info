import argparse
import json
import sys
import os
from pwd import getpwuid

# FileInfo class
#
# Initialize the class with a root and optional print pretty flag
# Supporting validation of arguments/class initialization
# Build a Dictionay of files and directories
class FileInfo:

    # initialize with a root and optional print pretty flag
    def __init__(self,root,print_pretty):
        self.ARGS = {"root": root, "print_pretty": print_pretty}

    # Validation, root can't be None
    def validate_args(self):
        if self.ARGS["root"] == None:
            sys.exit(1)

    # get file owner using pwd
    def get_file_owner(self,filename):
        return getpwuid(os.stat(filename).st_uid).pw_name

    # get file owner using pwd
    def get_file_permissions(self,filename):
        return oct(os.stat(filename).st_mode)

    # recursive function to insert the directory key with 
    # appropriate files into the current dictionary
    def buildJson(self,current_key, current_dict, dirs, files):
        for key in current_dict:
            if key in current_key:
                current_dict[key] = self.buildJson(current_key, current_dict[key],dirs,files)
                return current_dict

        current_dict[current_key] = {}

        if (self.ARGS["print_pretty"]):
            print("\n\nList of contents of " + current_key)
            print("\nDirectories: " + ' '.join([str(directory) for directory in dirs]))

        # insert all file key values for each file
        for filename in files:

            file_dictionary = {"file name": filename}

            filepath = current_key + "/" + filename

            file_ = open(filepath, 'r', encoding='utf-8', errors='ignore')

            filesize = os.path.getsize(current_key + "/" + filename)
            file_dictionary["file size (bytes)"] = filesize

            fileowner = self.get_file_owner(filepath)
            file_dictionary["file owner"] = fileowner

            filepermissions = self.get_file_permissions(filepath)
            file_dictionary["file permissions (octal)"] = filepermissions

            content = "".join(file_.readlines())

            file_dictionary["file content"] = content

            file_.close()

            if (self.ARGS["print_pretty"]):
                print("\nFile " + filename)
                print("File Size (bytes): " + str(filesize))
                print("File Owner: " + fileowner)
                print("File Permissions (octal): " + filepermissions)
                print("File Contents: \n")
                print("-----Content Begin-----")
                print(content)
                print("-----Content End-----")

            current_dict[current_key][filepath] = file_dictionary

        return current_dict


    # Main function to call
    # Call with an initialized FileInfo class
    # Output will be a dictionary of your filesystem from a given root
    def build_and_write_to_json(self):
        path_dict = {}
        for path, dirs, files in os.walk(self.ARGS["root"]):
            path_from_root = path.lstrip(self.ARGS["root"])
            paths_preceding = path_from_root.split("/")

            path_dict = self.buildJson(path, path_dict, dirs, files)
        return path_dict

    # Call to convert a dictionary to a json string
    def create_json_string(self, path_dict):
        return json.dumps(path_dict, indent=2)

if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser(description='Provide a root directory and optional printing setting')
    parser.add_argument('--root', default=None)
    parser.add_argument('--print-pretty', action='store_true')
    args = parser.parse_args()

    # initialize class
    file_info = FileInfo(args.root, args.print_pretty)

    # validate arguments
    file_info.validate_args()

    # Get dictionary of your filesystem from a given root
    path_dict = file_info.build_and_write_to_json()

    # Print the JSON if we are not pretty printing
    if not args.print_pretty:
        print(file_info.create_json_string(path_dict))

    sys.exit(0)


    