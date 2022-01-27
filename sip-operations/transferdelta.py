#!/usr/bin/env python3

import argparse
import itertools
import sys
import os.path

from types import SimpleNamespace


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--transfer", required=True)
    parser.add_argument("--old_transfer", required=True, nargs='+')
    parser.add_argument("--dest", required=True)
    args = parser.parse_args()

    generate_transfer_delta(args.transfer, args.old_transfer, args.dest)

def generate_transfer_delta(transfer, old_transfers, dest):
    old_lidvids = set(itertools.chain.from_iterable(read_transfer(x) for x in old_transfers))
    deltas = (x for x in read_transfer(transfer) if x.lidvid not in old_lidvids)
    delta_lines = (f"{x.lidvid}\r\n" for x in deltas)
    
    output_path = os.path.join(dest, os.path.basename(transfer))
    with open(output_path, "w") as out:
        for line in delta_lines:
            out.write(line)

def read_transfer(file_path: str):
    return (parse_transfer_line(line) for line in open(file_path))

def parse_transfer_line(line: str):
    lidvid = line.strip()
    return SimpleNamespace(
        lidvid=lidvid
    )


if __name__ == '__main__':
    sys.exit(main())