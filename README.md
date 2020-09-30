# Python  Homework

This script is a Python implementation for finding duplicate files in given directory. It does that by hashing the content of every file in given directory and comparing the hash value of each file. The dictionary containg the hash value and files is later on written to meta.json file as json

### Usage
Make the script executable with `chmod a+x detector.py`
Used with single or multiple directories as argument:
```bash
./detector.py <dir> [dir2...]
```
'--size' as argument to show the size of the duplicate files in parentheses:

```bash
./detector.py --size <dir>

# Example:
./detector.py --size ./a/ 
Found 1 duplicate:
a.txt = d/b.txt (16) (50d858e0985ecc7f60418aaf0cc5ab587f42c2570a884095 a9e8ccacd0f6545c)

```
'--new' as argument to show the files missing in the previous directory:

```bash
./detector.py --new <dir>

# Example:
./detector.py --new ./a/ ./b/
c.txt in ./b/ is new (not found in ./a/)
Found 1 duplicate:
a.txt = d/b.txt (50d858e0985ecc7f60418aaf0cc5ab587f42c2570a884095 a9e8ccacd0f6545c)
```

'--delete' as argument to delete the duplicate files from directory:

```bash
./detector.py --delete <dir>

# Example:
./detector.py --delete ./a/ 
Found 1 duplicate:
a.txt = d/b.txt (50d858e0985ecc7f60418aaf0cc5ab587f42c2570a884095 a9e8ccacd0f6545c)
Removing d/b.txt
``` 

### Unit tests
Can be run with `pytest` or `python3 test_detector.py`
