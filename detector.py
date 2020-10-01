#!/usr/bin/python3

import argparse
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
    detect.write_to_file()


args = parser.parse_args()
run_detector(args)
