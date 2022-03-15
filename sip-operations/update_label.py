#!/usr/bin/env python3

import sys
import argparse
import os.path
import os
import re
import shutil

import aiplabel
import siplabel

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sip_dir", required=True)
    args = parser.parse_args()

    dest = args.sip_dir
    os.makedirs(dest, exist_ok=True)

    sip = find_file(args.sip_dir, ".*sip.*tab")
    transfer = find_file(args.sip_dir, ".*transfer.*tab")
    checksum = find_file(args.sip_dir, ".*checksum.*tab")

    aip_label_src, aip_label = backup_label(find_file(args.sip_dir, ".*aip.*xml"))
    aiplabel.update_aip_checksums(checksum, transfer, aip_label_src, aip_label)

    sip_label_src, sip_label = backup_label(find_file(args.sip_dir, ".*sip.*xml"))
    siplabel.update_sip_checksums(sip, sip_label_src, aip_label, sip_label)

    return 0

def find_files(dirname, pattern):
    return [os.path.join(dirname, x) for x in os.listdir(dirname) if re.match(pattern, x)]

def find_file(dirname, pattern):
    candidates = [os.path.join(dirname, x) for x in os.listdir(dirname) if re.match(pattern, x)]
    if len(candidates) == 1:
        return candidates[0]
    raise Exception(f"more than one file matches this pattern: {pattern}")

def backup_label(filepath):
    dest_file = filepath.replace(".xml", ".old.xml")
    shutil.copyfile(filepath, dest_file)
    return dest_file, filepath


if __name__ == '__main__':
    sys.exit(main())