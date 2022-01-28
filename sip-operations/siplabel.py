#!/usr/bin/env python3

import argparse
import sys
import os.path
import tempfile
import shutil
import re
import functools
import hashlib


from types import SimpleNamespace
from lxml import etree


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sip", required=True)
    parser.add_argument("--aiplabel", required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--dest", required=True)

    args = parser.parse_args()

    gen_sip_label(args.sip, args.label, args.aiplabel, args.dest)

    return 0

def gen_sip_label(sip, siplabel, aiplabel, dest):
    sip_stats = get_stats(sip)
    aip_stats = get_stats(aiplabel)

    ns="{http://pds.nasa.gov/pds4/pds/v1}"
    with open(siplabel) as xml:
        label:etree._ElementTree = etree.parse(xml)

    info_package = label.find(f"{ns}Information_Package_Component_Deep_Archive")
    info_package.find(f"{ns}manifest_checksum").text = sip_stats.checksum
    info_package.find(f"{ns}aip_label_checksum").text = aip_stats.checksum
    
    file_area = info_package.find(f"{ns}File_Area_SIP_Deep_Archive")
    manifest = file_area.find(f"{ns}Manifest_SIP_Deep_Archive")
    manifest.find(f"{ns}object_length").text = sip_stats.filesize
    manifest.find(f"{ns}records").text = sip_stats.linecount
    file = file_area.find(f"{ns}File")
    file.find(f"{ns}file_size").text = sip_stats.filesize
    file.find(f"{ns}records").text = sip_stats.linecount


    output_path = os.path.join(dest, os.path.basename(siplabel))
    label.write(output_path, encoding="utf-8", xml_declaration=True, pretty_print=True)



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
