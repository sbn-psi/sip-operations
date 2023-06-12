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

def generate_transfer_delta(transfer, old_transfers, dest, suffix, bundle_lidvid, excluded_lidvids=[]):
    '''Generates the delta for the transfer manifest'''
    old_entries = read_old_entries(old_transfers, bundle_lidvid)
    deltas = (x for x in read_transfer(transfer) 
        if (x.lidvid, x.filename) not in old_entries 
        and x.lidvid not in excluded_lidvids)
    delta_lines = (f"{x.lidvid:255}{x.filename:255}\r\n" for x in deltas)
    
    output_path = os.path.join(dest, os.path.basename(transfer).replace("transfer_manifest", f"transfer_manifest_{suffix}"))
    with open(output_path, "w") as out:
        for line in delta_lines:
            out.write(line)

    return output_path

def read_old_entries(old_transfers, bundle_lidvid):
    '''Reads LIDVID and filename from a list of previous transfer manifests'''
    return set(itertools.chain.from_iterable(
        ((t.lidvid, t.filename) for t in read_transfer(x) if not t.lidvid == bundle_lidvid)
        for x in old_transfers))

def read_transfer(file_path: str):
    '''Reads a transfer manifest'''
    return (parse_transfer_line(line.strip("\r\n")) for line in open(file_path))

def parse_transfer_line(line: str):
    '''Converts a line of text into a transfer manifest entry'''
    return SimpleNamespace(
        lidvid=line[:255].strip(),
        filename=line[256:].strip()
    )

def get_superseded_collection_lidvids(file_path):
    '''Finds collection LIDVIDS that are not the latest version. These will be excluded'''
    parsed_lidvids = (parse_lidvid(x.lidvid) for x in read_transfer(file_path))
    collection_descs = sorted((x for x in parsed_lidvids if x.collection is not None), key=lambda x: x.collection)
    collections_by_id = itertools.groupby(collection_descs, lambda x: x.collection)
    latest_collections = (max(collections, key = lambda x: (x.major, x.minor)) for _, collections in collections_by_id)
    latest_collection_lidvids = set(x.lidvid for x in latest_collections)
    return set(x.lidvid for x in collection_descs if x.lidvid not in latest_collection_lidvids)

def get_superseded_collection_filenames(file_path, superseded_collection_lidvids):
    '''Finds the filenames for collections that are not the latest version'''
    return set(x.filename for x in read_transfer(file_path) if x.lidvid in superseded_collection_lidvids)

def parse_lidvid(lidvid):
    '''Interprets a LIDVID'''
    lid, vid = lidvid.split('::')
    tokens = lid.split(":")
    collection = tokens[4] if len(tokens) == 5 else None
    major, minor = [int(x) for x in vid.split('.')]
    return SimpleNamespace(
        lidvid = lidvid,
        collection = collection,
        lid = lid,
        vid = vid,
        major = major,
        minor = minor
    )

if __name__ == '__main__':
    sys.exit(main())