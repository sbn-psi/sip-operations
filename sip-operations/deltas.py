#!/usr/bin/env python3

import sys
import argparse
import os.path
import os
import re
import datetime

import transferdelta
import sipdelta
import aiplabel
import siplabel
import checksumdelta

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--old_dir")
    parser.add_argument("--new_dir")
    args = parser.parse_args()

    dest = os.path.join(args.new_dir, "deltas")
    os.makedirs(dest, exist_ok=True)

    datestr = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    suffix = f"delta_{datestr}"

    old_sips = find_files(args.old_dir, ".*sip.*tab")
    sip = find_files(args.new_dir, ".*sip.*tab")[0]
    delta_sip = sipdelta.generate_delta(old_sips, sip, dest, suffix)

    old_transfers = find_files(args.old_dir, ".*transfer.*tab")
    transfer = find_files(args.new_dir, ".*transfer.*tab")[0]
    delta_transfer = transferdelta.generate_transfer_delta(transfer, old_transfers, dest, suffix)

    old_checksums = find_files(args.old_dir, ".*checksum.*tab")
    checksum = find_files(args.new_dir, ".*checksum.*tab")[0]
    delta_checksum = checksumdelta.generate_checksum_delta(checksum, old_checksums, dest, suffix)

    aip_label = find_files(args.new_dir, ".*aip.*xml")[0]
    aip_lidvid, generated_aip_label = aiplabel.gen_aip_label(delta_checksum, delta_transfer, aip_label, dest, suffix)

    sip_label = find_files(args.new_dir, ".*sip.*xml")[0]
    siplabel.gen_sip_label(delta_sip, sip_label, generated_aip_label, aip_lidvid, dest, suffix)

    return 0

def find_files(dirname, pattern):
    return [os.path.join(dirname, x) for x in os.listdir(dirname) if re.match(pattern, x)]

if __name__ == '__main__':
    sys.exit(main())