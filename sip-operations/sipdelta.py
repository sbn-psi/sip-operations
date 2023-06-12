#!/usr/bin/env python3

import sys
import argparse
import itertools
import os.path

OUT_FORMAT="{checksum}\t{checksum_type}\t{url}\t{lidvid}\r\n"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--old_sip", required=True, nargs="+")
    parser.add_argument("--sip", required=True)
    parser.add_argument("--dest", required=True)
    parser.add_argument("--suffix", required=True)
    #parser.add_argument("--label", required=True)
    #parser.add_argument("--output_label", required=True)
    args = parser.parse_args()

    generate_delta(args.old_sip, args.sip, args.dest, args.suffix)

    return 0

 

def generate_delta(old_sips, sip, dest, suffix, bundle_lidvid, excluded_lidvids=[]):
    '''Generates the SIP delta'''
    old_lids = read_old_entries(old_sips, bundle_lidvid)
    #print(old_lids)
    deltas = (x for x in read_sip(sip) if x["url"] not in old_lids and x["lidvid"] not in excluded_lidvids)
    delta_lines = (OUT_FORMAT.format(**x) for x in deltas)
    
    output_file = os.path.basename(sip).replace("sip", f"sip_{suffix}")
    output_path = os.path.join(dest, output_file)
    with open(output_path, "w") as out:
        for line in delta_lines:
            out.write(line)

    return output_path

def read_old_entries(old_sips, bundle_lidvid):
    '''Reads LIDs from the previous SIP files'''
    return set(l for l in itertools.chain.from_iterable(extract_lids(x) for x in old_sips) if not l == bundle_lidvid)

def extract_lids(sip):
    '''Reads LIDs from a SIP file'''
    return (x["url"] for x in read_sip(sip))

def read_sip(file_path: str):
    '''Reads entries from a SIP file'''
    return (parse_sip_line(line) for line in open(file_path))

def parse_sip_line(line: str):
    '''Converts a raw text line to a SIP entry'''
    checksum, checksum_type, url, lidvid = line.strip().split("\t")
    return {
        "url": url,
        "lidvid": lidvid,
        "checksum": checksum,
        "checksum_type" : checksum_type
    }

if __name__ == '__main__':
    sys.exit(main())