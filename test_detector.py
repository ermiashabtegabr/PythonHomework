import pytest
import os
import shutil
from detect import Detect


dir_list = []
files_list = []

test_dir = 'test_dir'
test_subdir = test_dir + '/test_subdir'
test_dir2 = 'test_dir2'
test_subdir2 = test_dir2 + '/test_subdir2'

dir_list.append(test_dir)
dir_list.append(test_dir2)

a = test_dir + '/a.txt'
b = test_dir + '/b.txt'
c = test_subdir + '/c.txt'
d = test_dir2 + '/a.txt'
e = test_dir2 + '/b.txt'
f = test_subdir2 + '/f.txt'

# Removing the root from filename, d and e are not included since their content is unique
a_filename = a[a.find('/'):]
b_filename = b[b.find('/'):]
c_filename = c[c.find('/'):]
d_filename = d[d.find('/'):]
f_filename = f[f.find('/'):]

# Adding to files list to separate the hash keys and the filename keys
files_list.append(a_filename)
files_list.append(b_filename)
files_list.append(c_filename)
files_list.append(f_filename)

# Making directories and subdirectories
if not os.path.exists(test_dir):
    os.makedirs(test_dir)

if not os.path.exists(test_dir2):
    os.makedirs(test_dir2)

if not os.path.exists(test_subdir2):
    os.makedirs(test_subdir2)

if not os.path.exists(test_subdir):
    os.makedirs(test_subdir)

# Making files and adding content, where some of the files have the same content
file = open(a, "w")
file.write("This is file a")
file.close()

file = open(b, "w")
file.write("And this is file b")
file.close()

file = open(c, "w")
file.write("This is file a")
file.close()

file = open(d, "w")
file.write("This is file a")
file.close()

file = open(e, "w")
file.write("Is this also file a?")
file.close()

file = open(f, "w")
file.write("And this is file b")
file.close()

detect = Detect(dir_list, show_new=False,
                show_size=True, delete_duplicates=False)


def test_duplicates():
    detect.iterate_directories()
    hash_value = detect.hash_dict

    # There are five files with the same content in both directories,
    # and these are dir1/a, dir1/c, dir2/a and dir1/b, dir2/f.
    for value in hash_value.values():
        if len(value) > 1 and value[0] in files_list:
            # If the value in the dictionary has more than one element,
            # then either dir1/a, dir1/c, dir2/a or dir1/b, dir2/f are in the list
            duplicates = (
                a_filename in hash_value and c_filename in hash_value and d_filename in hash_value)
            duplicates2 = (
                b_filename in hash_value and f_filename in hash_value)
            assert duplicates or duplicates2

    # Asserting that there are two files with the same name, in this case a.txt and b.txt
    assert len(hash_value[a_filename]) == 2
    assert len(hash_value[b_filename]) == 2

    # Remove the files and directories created
    shutil.rmtree(test_dir)
    shutil.rmtree(test_dir2)
