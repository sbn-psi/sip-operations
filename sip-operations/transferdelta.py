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
    parser.add_argument("--suffix", required=True)
    args = parser.parse_args()

    generate_transfer_delta(args.transfer, args.old_transfer, args.dest, args.suffix)

def generate_transfer_delta(transfer, old_transfers, dest, suffix):
    old_entries = set(itertools.chain.from_iterable(
        ((t.lidvid, t.filename) for t in read_transfer(x))
        for x in old_transfers))
    deltas = (x for x in read_transfer(transfer) if (x.lidvid, x.filename) not in old_entries)
    delta_lines = (f"{x.lidvid:255}{x.filename:255}\r\n" for x in deltas)
    
    output_path = os.path.join(dest, os.path.basename(transfer).replace("transfer_manifest", f"transfer_manifest_{suffix}"))
    with open(output_path, "w") as out:
        for line in delta_lines:
            out.write(line)

    return output_path

def read_transfer(file_path: str):
    return (parse_transfer_line(line.strip("\r\n")) for line in open(file_path))

def parse_transfer_line(line: str):
    return SimpleNamespace(
        lidvid=line[:255].strip(),
        filename=line[256:].strip()
    )


if __name__ == '__main__':
    sys.exit(main())