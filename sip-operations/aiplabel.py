#!/usr/bin/env python3

import argparse
from cmath import inf
import sys
import os.path
import tempfile
import shutil
import re
import functools
import hashlib
from xml.etree.ElementTree import ElementTree
from lxml import etree
from types import SimpleNamespace



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--transfer", required=True)
    parser.add_argument("--checksum", required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--dest", required=True)

    args = parser.parse_args()

    checksum_stats = get_stats(args.checksum)
    transfer_stats = get_stats(args.transfer)

    ns="{http://pds.nasa.gov/pds4/pds/v1}"
    with open(args.label) as xml:
        label:etree._ElementTree = etree.parse(xml)

    info_package = label.find(f"{ns}Information_Package_Component")
    info_package.find(f"{ns}checksum_manifest_checksum").text = checksum_stats.checksum
    info_package.find(f"{ns}transfer_manifest_checksum").text = transfer_stats.checksum
    
    file_area_checksum_manifest = info_package.find(f"{ns}File_Area_Checksum_Manifest")
    checksum_manifest = file_area_checksum_manifest.find(f"{ns}Checksum_Manifest")
    checksum_manifest.find(f"{ns}object_length").text = checksum_stats.filesize
    c_file = file_area_checksum_manifest.find(f"{ns}File")
    c_file.find(f"{ns}file_size").text = checksum_stats.filesize
    c_file.find(f"{ns}records").text = checksum_stats.linecount

    file_area_transfer_manifest = info_package.find(f"{ns}File_Area_Transfer_Manifest")
    transfer_manifest = file_area_transfer_manifest.find(f"{ns}Transfer_Manifest")
    transfer_manifest.find(f"{ns}records").text = transfer_stats.linecount
    t_file = file_area_transfer_manifest.find(f"{ns}File")
    t_file.find(f"{ns}file_size").text = transfer_stats.filesize
    t_file.find(f"{ns}records").text = transfer_stats.linecount

    output_path = os.path.join(args.dest, os.path.basename(args.label))
    label.write(output_path, encoding="utf-8", xml_declaration=True, pretty_print=True)

    return 0

def get_stats(filepath):
    filesize = os.path.getsize(filepath)
    linecount = sum(1 for x in open(filepath))
    checksum = get_checksum(filepath)
    return SimpleNamespace(
        filesize=str(filesize), 
        linecount=str(linecount), 
        checksum=checksum)

def get_checksum(filepath):
    with(open(filepath, "rb") as file):
        md5 = hashlib.md5()
        md5.update(file.read())
        return md5.hexdigest()


if __name__ == '__main__':
    sys.exit(main())
