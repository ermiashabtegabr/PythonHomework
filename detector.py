#!/usr/bin/python3

import os
import sys
import hashlib
import json
import base64
# from os.path import join, getsize

hash_dict = {}


def iterate_directories(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            filename = filepath.replace(directory, '')
            read_from_file_and_hash_content(filepath, filename)


def read_from_file_and_hash_content(pathname, filename):
    file_content = ''
    with open(pathname, 'r') as f:
        file_content += f.read()

    byte_value = str.encode(file_content)
    h = hashlib.sha256()
    h.update(byte_value)
    hash_value = h.hexdigest()

    if hash_value in hash_dict:
        hash_dict[hash_value].append(filename)
    else:
        hash_dict[hash_value] = [filename]

    hash_dict[filename] = [hash_value]


def find_duplicates():
    found_duplicates = False
    for key, value in hash_dict.items():
        if len(value) > 1:
            first_file = value[0]
            rest_of_the_files = ','.join(first_file[1:]) if len(value) > 2 else value[1]
            output(first_file, rest_of_the_files, key)
            found_duplicates = True

    if not found_duplicates:
        print('There are no duplicates in this directory')


def output(first_file, rest_of_the_files, hash_values):
    print(f'Found duplicates')
    print(f'{first_file} = {rest_of_the_files}', end=' ')
    print(f'({hash_values})')


def run_program(directory):
    iterate_directories(directory)
    f = open('meta.json', 'w')
    json.dump(hash_dict, f, ensure_ascii=False, indent=4)
    find_duplicates()


args = sys.argv
run_program(args[1])


# print(sum(getsize(join(root, name)) for name in files), end=" ")
# https: // stackoverflow.com/questions/26587037/how-can-get-a-list-of-files-in-a-specific-directory-ignoring-the-symbolic-links
