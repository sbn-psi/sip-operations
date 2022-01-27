#!/usr/bin/env python3

import argparse
import itertools
import sys
import os.path

from types import SimpleNamespace


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--transfer", required=True)
    parser.add_argument("--checksum", required=True)
    parser.add_argument("--old_transfer", required=True, nargs='+')
    parser.add_argument("--old_checksum", required=True, nargs='+')
    parser.add_argument("--dest", required=True)
    args = parser.parse_args()

    generate_checksum_delta(args.checksum, args.old_checksum, args.dest)
    generate_transfer_delta(args.transfer, args.old_transfer, args.dest)

def generate_checksum_delta(checksum, old_checksums, dest):
    old_entries = set(itertools.chain.from_iterable(read_checksum(x) for x in old_checksums))
    deltas = (x for x in read_checksum(checksum) if x not in old_entries)
    delta_lines = (f"{x.checksum}\t{x.filename}\r\n" for x in deltas)

    output_path = os.path.join(dest, os.path.basename(checksum))
    with open(output_path, "w") as out:
        for line in delta_lines:
            out.write(line)

def read_checksum(file_path: str):
    return (parse_checksum_line(line) for line in open(file_path))

def parse_checksum_line(line:str):
    checksum, filename = line.strip().split("\t")
    return SimpleNamespace(
        checksum=checksum,
        filename=filename
    )

def generate_transfer_delta(transfer, old_transfers, dest):
    old_lidvids = set(itertools.chain.from_iterable(extract_transfer_lidvids(x) for x in old_transfers))
    deltas = (x for x in read_transfer(transfer) if x.lidvid not in old_lidvids)
    delta_lines = (f"{x.lidvid}\r\n" for x in deltas)
    
    output_path = os.path.join(dest, os.path.basename(transfer))
    with open(output_path, "w") as out:
        for line in delta_lines:
            out.write(line)

def extract_transfer_lidvids(filepath):
    return (x.lidvid for x in read_checksum(filepath))

def read_transfer(file_path: str):
    return (parse_transfer_line(line) for line in open(file_path))

def parse_transfer_line(line: str):
    lidvid = line.strip()
    return SimpleNamespace(
        lidvid=lidvid
    )


if __name__ == '__main__':
    sys.exit(main())