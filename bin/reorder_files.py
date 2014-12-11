#!/usr/bin/python2.7
import argparse
import os
import re
import sys
import itertools


def get_parser():
    parser = argparse.ArgumentParser(description='Rename numeric filename prefixes.')
    parser.add_argument('path', help='filename to rename')
    parser.add_argument('new_prefix', type=int, help='New prefix')
    return parser


def parse_int_prefix(x):
    try:
        return int(re.search('(^[0-9]*)', x).group(0))
    except ValueError:
        # Default photo to start of list if it isn't prefixed
        return -1


def get_insertion_index(sorted_files, new_prefix):
    for i, filename in enumerate(sorted_files):
        if parse_int_prefix(filename) >= new_prefix:
            return i
    return len(sorted_files)


def main():
    parser = get_parser()
    args = parser.parse_args()

    dirname = os.path.dirname(args.path) or '.'
    filename = os.path.basename(args.path)
    files = os.listdir(dirname)

    tmp_suffix = '.rename.swp'
    if any(x.endswith(tmp_suffix) for x in files):
        print >> sys.stderr, 'Unable to proceed with %s files present' % tmp_suffix
        sys.exit(1)

    files = sorted((x for x in files if x != filename), key=parse_int_prefix)
    i = get_insertion_index(files, args.new_prefix)
    files[i:i] = [filename]
    renamed_files = [re.sub('^[0-9]*', '%02d' %(i+1,), x) for i, x in enumerate(files)]

    for filename in files:
        os.rename(os.path.join(dirname, filename), os.path.join(dirname, filename + tmp_suffix))

    for current_name, new_name in itertools.izip(files, renamed_files):
        if current_name != new_name:
            print 'renaming %s to %s' % (current_name, new_name)
        os.rename(os.path.join(dirname, current_name + tmp_suffix), os.path.join(dirname, new_name))


if __name__ == '__main__':
    main()
