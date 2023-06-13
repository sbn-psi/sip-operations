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
    parser.add_argument("--bundle_url", required=False, default="https://sbnarchive.psi.edu/pds4/surveys/gbo.ast.catalina.survey/bundle_gbo.ast.catalina.survey_v1.0.xml")
    args = parser.parse_args()

    generate_deltas(args.old_dir, args.new_dir, args.bundle_label, args.bundle_url)

    return 0

def generate_deltas(old_dir, new_dir, bundle_label, bundle_url):
    '''Generates deltas for the SIP, AIP and checksum manifest'''
    dest = os.path.join(new_dir, "deltas")
    os.makedirs(dest, exist_ok=True)

    datestr = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    suffix = f"delta_{datestr}"


    transfer = find_files(new_dir, ".*transfer.*tab$")[0]
    superseded_collection_lidvids = transferdelta.get_superseded_collection_lidvids(transfer)

    delta_checksum = generate_checksum_delta(transfer, superseded_collection_lidvids, old_dir, new_dir, dest, suffix, bundle_label)
    aip_lidvid, generated_aip_label = generate_aip_delta(bundle_label, transfer, dest, suffix, superseded_collection_lidvids, old_dir, new_dir, delta_checksum)
    delta_sip = gen_sip_delta(old_dir, new_dir, dest, suffix, bundle_url, superseded_collection_lidvids)

    sip_label = find_files(new_dir, ".*sip.*xml$")[0]
    siplabel.gen_sip_label(delta_sip, sip_label, generated_aip_label, aip_lidvid, dest, suffix)


def generate_checksum_delta(transfer, superseded_collection_lidvids, old_dir, new_dir, dest, suffix, bundle_label):
    '''Generates the delta for the checkusm manifest'''
    superseded_collection_filenames = transferdelta.get_superseded_collection_filenames(transfer, superseded_collection_lidvids)
    old_checksums = find_files(old_dir, ".*checksum.*tab$")
    checksum = find_files(new_dir, ".*checksum.*tab$")[0]
    return checksumdelta.generate_checksum_delta(checksum, old_checksums, dest, suffix, bundle_label, superseded_collection_filenames)

def generate_aip_delta(bundle_label, transfer, dest, suffix, superseded_collection_lidvids, old_dir, new_dir, delta_checksum):
    '''Generates the delta for the AIP'''
    bundle_lidvid = extract_lidvid(bundle_label)
    old_transfers = find_files(old_dir, ".*transfer.*tab$")
    delta_transfer = transferdelta.generate_transfer_delta(transfer, old_transfers, dest, suffix, bundle_lidvid, superseded_collection_lidvids)
    aip_label = find_files(new_dir, ".*aip.*xml$")[0]
    return aiplabel.gen_aip_label(delta_checksum, delta_transfer, aip_label, dest, suffix)

def gen_sip_delta(old_dir, new_dir, dest, suffix, bundle_url, superseded_collection_lidvids):
    '''Generates the delta for the SIP'''
    old_sips = find_files(old_dir, ".*sip.*tab$")
    sip = find_files(new_dir, ".*sip.*tab$")[0]
    return sipdelta.generate_delta(old_sips, sip, dest, suffix, bundle_url, superseded_collection_lidvids)


def find_files(dirname, pattern):
    '''Gets a list of files in the supplied directory that match the specified pattern'''
    return [os.path.join(dirname, x) for x in os.listdir(dirname) if re.match(pattern, x)]

def extract_lidvid(bundle_file):
    '''Gets the LIDVID from the label'''
    ns="{http://pds.nasa.gov/pds4/pds/v1}"
    with open(bundle_file) as xml:
        label:etree._ElementTree = etree.parse(xml)

    id_area = label.find(f"{ns}Identification_Area")
    lid = id_area.find(f"{ns}logical_identifier").text
    vid = id_area.find(f"{ns}version_id").text
    return f"{lid}::{vid}"



if __name__ == '__main__':
    sys.exit(main())