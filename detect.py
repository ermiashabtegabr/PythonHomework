import os
import sys
import json
import hashlib
from os.path import join, getsize


class Detect:

    def __init__(self, directory, show_new, show_size, delete_duplicates):
        # Given directory
        self.directory = directory

        # Flags
        self.show_new = show_new
        self.show_size = show_size
        self.delete_duplicates = delete_duplicates

        # Hash dictionary
        self.hash_dict = {}

        # Has a filename as key and file size as value. Used for printing file size.
        self.file_size = {}

        # Contains all files in given directory. Used for separating the hash
        # and filename key values
        self.files = []

        # Contains duplicate files to be removed
        self.files_to_remove = []

    def iterate_directories(self):
        """
        Iterates through files in the given directory and its subdirectories,
        and calls read_from_file_and_hash_content function with the path for 
        each file.

        """
        for i in range(len(self.directory)):
            directory = self.directory[i]

            if not os.path.isdir(directory):
                print(f'{directory} is not a directory')
                continue

            for root, dirs, files in os.walk(directory):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    filename_without_root = filepath[filepath.find('/'):]

                    # If the self.show_new variable it true, then the files not present in the previous
                    # directory are printed out

                    # If the  filename is not a key in the hash dictionary, it is not in the previous directory
                    if self.show_new and i > 0:
                        self.check_if_new_file(
                            filename, directory, self.directory[i-1])

                    self.files.append(filename_without_root)
                    self.read_from_file_and_hash_content(
                        filepath, filename_without_root)

    def check_if_new_file(self, filename, current_dir, previous_dir):
        """
        Checks if filename is a key in the hash dictionary or a subtring of the key, 
        and if that is the case then the file is not new. Otherwise, if the filename 
        is not a key or a substring of a key in the dictionary then it is a new file, 
        and the filename is printed out along with the current and previous directory.

        Args:
            filename (str): filename to check if the file is in the previous dir
            current_dir (str): name of the directory current going through 
            previous_dir (str): name of the previous directory 
        """

        for key in self.hash_dict.keys():
            if filename in key:
                return

        print(f'{filename} in {current_dir} is new (not found in {previous_dir})')

    def read_from_file_and_hash_content(self, pathname, filename):
        """
        Goes through the content of each file and hashes the value, 
        and addes the hash values to dict.

        Args:
            pathname (str): path for the file to go through (contains the root directory name).
            filename (str): name of the file (does not contain the root direcoty name).
        """

        file_content = ''
        try:
            with open(pathname, 'r') as f:
                file_content += f.read()
        except Exception as arg:
            print(f'Exepction occurred: {arg}')

        # Hashing the file content
        byte_value = str.encode(file_content)
        h = hashlib.sha256()
        h.update(byte_value)
        hash_value = h.hexdigest()

        # If the hash already exists as key value then it is a duplicate file
        if hash_value in self.hash_dict:
            self.hash_dict[hash_value].append(filename)
            self.files_to_remove.append(pathname)

            # Adding the size of the duplicate files to dictionary.
            # Only adding the size of one of these files since all have the same size
            if filename not in self.file_size:
                self.file_size[filename] = os.path.getsize(pathname)

        else:
            self.hash_dict[hash_value] = [filename]

        if filename in self.hash_dict:
            # If there are files with the same filename
            self.hash_dict[filename].append(hash_value)
        else:
            self.hash_dict[filename] = [hash_value]

    def find_duplicates(self):
        """
        Goes through the values in the hash dictionary and checks if there is a hash key
        with value of more than one filename. If that is the case then those files have 
        have the same content. 

        """
        found_duplicates = False
        for key, value in self.hash_dict.items():

            # If the value is a list of filenames (are in self.files) and there are more than
            # one elements, then these files are duplicates

            if len(value) > 1 and value[0] in self.files:
                self.output(value, key)
                found_duplicates = True

        if self.delete_duplicates:
            self.delete_duplicates_from_directories()

        if not found_duplicates:
            print('There are no duplicates in given directory')

    def get_file_size(self, files_list):
        """
        Goes through a list of files with the same content and returns the size 
        using self.file_size.

        Args:
            files_list (list): list containing filenames where these files have the same content.

        Returns:
            int: the size of files given as input.
        """
        for files in files_list:
            if files in self.file_size:
                return self.file_size[files]

    def delete_duplicates_from_directories(self):
        """
        Deletes the duplicate files leaving one file with unique content remaning
        """
        for filepath in self.files_to_remove:
            os.remove(filepath)
            print(f'Removing {filepath}')

    def output(self, files_list, hash_values):
        """
        Output of the duplicates in the given directory and includes the 
        size of the files if --size flag was included in the command line

        Args:
            files_list (list): list of filenames with the same content 
            hash_values (hex): the hash value of the files
        """
        print(f'Found duplicates')

        first_file = files_list[0]
        rest_of_the_files = ', '.join(files_list[1:]) if len(
            files_list) > 2 else files_list[1]

        print(f'{first_file} = {rest_of_the_files}', end=' ')

        if self.show_size:
            print(f'(size: {self.get_file_size(files_list)} bytes)')

        print(f'Hash value: ({hash_values})\n\n')

    def write_to_file(self):
        """
        Writes the hash dictionary to a json file
        """
        f = open('meta.json', 'w')
        json.dump(self.hash_dict, f, ensure_ascii=False, indent=4)
        f.close()
