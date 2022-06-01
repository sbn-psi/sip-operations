#!/usr/bin/env python3

import sys
import argparse
import os.path
import os
import re
import datetime

from lxml import etree


import transferdelta
import sipdelta
import aiplabel
import siplabel
import checksumdelta

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--old_dir", required=True)
    parser.add_argument("--new_dir", required=True)
    parser.add_argument("--bundle_label", required=True)
    args = parser.parse_args()

    dest = os.path.join(args.new_dir, "deltas")
    os.makedirs(dest, exist_ok=True)

    datestr = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    suffix = f"delta_{datestr}"

    bundle_lidvid = extract_lidvid(args.bundle_label)
    bundle_url="https://sbnarchive.psi.edu/pds4/surveys/gbo.ast.catalina.survey/bundle_gbo.ast.catalina.survey_v1.0.xml"

    old_sips = find_files(args.old_dir, ".*sip.*tab")
    sip = find_files(args.new_dir, ".*sip.*tab")[0]
    delta_sip = sipdelta.generate_delta(old_sips, sip, dest, suffix, bundle_url)

    old_transfers = find_files(args.old_dir, ".*transfer.*tab")
    transfer = find_files(args.new_dir, ".*transfer.*tab")[0]
    delta_transfer = transferdelta.generate_transfer_delta(transfer, old_transfers, dest, suffix, bundle_lidvid)

    old_checksums = find_files(args.old_dir, ".*checksum.*tab")
    checksum = find_files(args.new_dir, ".*checksum.*tab")[0]
    delta_checksum = checksumdelta.generate_checksum_delta(checksum, old_checksums, dest, suffix, args.bundle_label)

    aip_label = find_files(args.new_dir, ".*aip.*xml")[0]
    aip_lidvid, generated_aip_label = aiplabel.gen_aip_label(delta_checksum, delta_transfer, aip_label, dest, suffix)

    sip_label = find_files(args.new_dir, ".*sip.*xml")[0]
    siplabel.gen_sip_label(delta_sip, sip_label, generated_aip_label, aip_lidvid, dest, suffix)

    return 0

def find_files(dirname, pattern):
    return [os.path.join(dirname, x) for x in os.listdir(dirname) if re.match(pattern, x)]

def extract_lidvid(bundle_file):
    ns="{http://pds.nasa.gov/pds4/pds/v1}"
    with open(bundle_file) as xml:
        label:etree._ElementTree = etree.parse(xml)

    id_area = label.find(f"{ns}Identification_Area")
    lid = id_area.find(f"{ns}logical_identifier").text
    vid = id_area.find(f"{ns}version_id").text
    return f"{lid}::{vid}"



if __name__ == '__main__':
    sys.exit(main())