#!/usr/bin/env python3

import sys
import argparse
import tempfile
import os.path
import shutil
from unittest import TestProgram

OUT_FORMAT="{checksum}\t{checksum_type}\t{url}\t{lidvid}\r\n"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--old_sip", required=True)
    parser.add_argument("--sip", required=True)
    #parser.add_argument("--label", required=True)
    #parser.add_argument("--output_label", required=True)
    args = parser.parse_args()

    old_lids = set(x["lidvid"] for x in read_sip(args.old_sip))
    deltas = (x for x in read_sip(args.sip) if x["lidvid"] not in old_lids)
    delta_lines = (OUT_FORMAT.format(**x) for x in deltas)

    
    _, output_path = tempfile.mkstemp()
    with open(output_path, "w") as out:
        for line in delta_lines:
            out.write(line)
    shutil.move(args.sip, args.sip + ".bak")
    shutil.copyfile(output_path , args.sip)

    return 0

def read_sip(file_path: str):
    return (parse_sip_line(line) for line in open(file_path))

def parse_sip_line(line: str):
    checksum, checksum_type, url, lidvid = line.strip().split("\t")
    return {
        "url": url,
        "lidvid": lidvid,
        "checksum": checksum,
        "checksum_type" : checksum_type
    }

if __name__ == '__main__':
    sys.exit(main())