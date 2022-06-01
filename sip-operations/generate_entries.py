#!/usr/bin/env python3

import argparse
import hashlib
from math import prod
import sys
from types import SimpleNamespace
import os.path
import itertools
import pds4


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dirname")
    parser.add_argument("--urlbase")
    args = parser.parse_args()
    products = (pds4.create_product(x) for x in pds4.find_all_labels(os.path.join(args.dirname)))
    entries = list(itertools.chain.from_iterable(generate_entries_for_product(product, args.urlbase, args.dirname) for product in products))
    checksums = (x.checksum for x in entries)
    open("checksum.txt","w").write("\n".join(checksums))
    transfers = (x.transfer for x in entries)
    open("transfer.txt","w").write("\n".join(transfers))
    sips = (x.sip for x in entries)
    open("sip.txt", "w").write("\n".join(sips))
        

def generate_entries_for_product(product, urlbase, basedir):
    dirname = os.path.dirname(product.label_file)
    files = (os.path.join(dirname, x) for x in product.data_files)
    yield generate_entries_for_file(product.label_file, product.lidvid(), urlbase, basedir)
    for file_path in files:
        yield generate_entries_for_file(file_path, product.lidvid(), urlbase, basedir)

def generate_entries_for_file(file_path, lidvid, urlbase, basedir):
    checksum = md5sum(file_path)
    url = f'{urlbase}/{file_path}'
    output_file_path = file_path.replace(f'{basedir}/', '')

    return SimpleNamespace(
        checksum = gen_checksum_manifest_entry(checksum, output_file_path),
        transfer = gen_transfer_manifest_entry(lidvid, f'/{output_file_path}'),
        sip = gen_sip_entry(checksum, url, lidvid)
    )
    

def gen_checksum_manifest_entry(checksum, file_path):
    return f'{checksum}\t{file_path}'

def gen_transfer_manifest_entry(lidvid, file_path):
    return f'{lidvid:255}{file_path:255}'

def gen_sip_entry(checksum, url, lidvid, algorithm='MD5'):
    return f'{checksum}\t{algorithm}\t{url}\t{lidvid}'

def discover_labels(label):
    return ""

def extract_lidvid(label):
    return ""

def build_file_list(label):
    return []

def md5sum(file_path):
    h = hashlib.md5()
    with open(file_path, "rb") as f:
        h.update(f.read())
        return h.hexdigest()

if __name__ == '__main__':
    sys.exit(main())