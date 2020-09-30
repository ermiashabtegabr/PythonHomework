#!/usr/bin/python3

import argparse
import json
from detect import Detect

parser = argparse.ArgumentParser(
    description='Find duplicate files in given directory',
    prog="./detector.py ",
)

parser.add_argument(
    'dir', 
    type=str, 
    nargs='+',
    help='a diretory with files to iterate through'
)

parser.add_argument(
    "--new",
    action='store_true',
    help="print files which are missing in the previous folders"
)

parser.add_argument(
    "--size",
    action='store_true',
    help="include the file size in the output"
)

parser.add_argument(
    "--delete",
    action='store_true',
    help="delete duplicate file from directory"
)


def run_detector(args):
    detect = Detect(args.dir, args.new, args.size, args.delete)
    detect.iterate_directories()
    detect.find_duplicates()
    hash_dict = detect.hash_dict
    f = open('meta.json', 'w')
    json.dump(hash_dict, f, ensure_ascii=False, indent=4)
    f.close()

args = parser.parse_args()
run_detector(args)



