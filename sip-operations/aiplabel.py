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

    gen_aip_label(args.checksum, args.transfer, args.label, args.dest)


    return 0

def gen_aip_label(checksum, transfer, aiplabel, dest, suffix):
    checksum_stats = get_stats(checksum)
    transfer_stats = get_stats(transfer)

    ns="{http://pds.nasa.gov/pds4/pds/v1}"
    with open(aiplabel) as xml:
        label:etree._ElementTree = etree.parse(xml)

    id_area = label.find(f"{ns}Identification_Area")
    lid_element = id_area.find(f"{ns}logical_identifier")
    new_lid = lid_element.text + "_" + suffix
    new_lidvid = f"{new_lid}::1.0"
    lid_element.text = new_lid

    info_package = label.find(f"{ns}Information_Package_Component")
    info_package.find(f"{ns}checksum_manifest_checksum").text = checksum_stats.checksum
    info_package.find(f"{ns}transfer_manifest_checksum").text = transfer_stats.checksum
    
    file_area_checksum_manifest = info_package.find(f"{ns}File_Area_Checksum_Manifest")
    checksum_manifest = file_area_checksum_manifest.find(f"{ns}Checksum_Manifest")
    checksum_manifest.find(f"{ns}object_length").text = checksum_stats.filesize
    c_file = file_area_checksum_manifest.find(f"{ns}File")
    c_file.find(f"{ns}file_size").text = checksum_stats.filesize
    c_file.find(f"{ns}records").text = checksum_stats.linecount
    c_file.find(f"{ns}file_name").text = os.path.basename(checksum)

    file_area_transfer_manifest = info_package.find(f"{ns}File_Area_Transfer_Manifest")
    transfer_manifest = file_area_transfer_manifest.find(f"{ns}Transfer_Manifest")
    transfer_manifest.find(f"{ns}records").text = transfer_stats.linecount
    t_file = file_area_transfer_manifest.find(f"{ns}File")
    t_file.find(f"{ns}file_size").text = transfer_stats.filesize
    t_file.find(f"{ns}records").text = transfer_stats.linecount
    t_file.find(f"{ns}file_name").text = os.path.basename(transfer)

    output_path = os.path.join(dest, os.path.basename(aiplabel).replace("aip", f"aip_{suffix}"))
    label.write(output_path, encoding="utf-8", xml_declaration=True, pretty_print=True)

    return new_lidvid, output_path


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
