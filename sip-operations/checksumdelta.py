#!/usr/bin/env python3

import argparse
import itertools
import sys
import os.path

from types import SimpleNamespace


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checksum", required=True)
    parser.add_argument("--old_checksum", required=True, nargs='+')
    parser.add_argument("--dest", required=True)
    parser.add_argument("--suffix", required=True)
    args = parser.parse_args()

    generate_checksum_delta(args.checksum, args.old_checksum, args.dest, args.suffix)

def generate_checksum_delta(checksum, old_checksums, dest, suffix, bundle_filename, excluded_filenames):
    '''
    Generates a the delta for the checksum manifests.
    The delta consists of all files in the "new" file for which there is not 
    a matching filename present in the "old" files.
    '''
    old_entries = read_old_entries(old_checksums, bundle_filename)
    deltas = (x for x in read_checksum(checksum) if x.filename not in old_entries and x.filename not in excluded_filenames)
    delta_lines = (f"{x.checksum}\t{x.filename}\r\n" for x in deltas)

    output_path = os.path.join(dest, os.path.basename(checksum).replace("checksum_manifest", f"checksum_manifest_{suffix}"))
    with open(output_path, "w") as out:
        for line in delta_lines:
            out.write(line)

    return output_path

def read_old_entries(old_checksums, bundle_filename):
    '''Reads the previous checksum manifests'''
    return set(itertools.chain.from_iterable(
        (c.filename for c in read_checksum(x)  if not os.path.basename(c.filename) == os.path.basename(bundle_filename)) 
        for x in old_checksums))

def read_checksum(file_path: str):
    '''Reads a single checksum manifest'''
    return (parse_checksum_line(line) for line in open(file_path))

def parse_checksum_line(line:str):
    '''Converts a text line into a checksum manifest entry'''
    checksum, filename = line.strip().split("\t")
    return SimpleNamespace(
        checksum=checksum,
        filename=filename
    )

if __name__ == '__main__':
    sys.exit(main())