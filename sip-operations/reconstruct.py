#!/usr/bin/env python3

import sys
import argparse
import typing

from dictops import patch_dict_list, dictify_file, join_dict_lists

TRANSFER_MANIFEST_COLUMNS=['lidvid', 'path']
CHECKSUM_MANIFEST_COLUMNS=['checksum', 'path']
SIP_COLUMNS=[]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sip", required=True)
    parser.add_argument("--checksum", required=True)
    parser.add_argument("--transfer", required=True)
    args = parser.parse_args()
    transfer_manifests = patch_dict_list(dictify_file(args.transfer, TRANSFER_MANIFEST_COLUMNS), "path", "path",lambda x: x.strip('/'))
    checksum_manifests = dictify_file(args.checksum, CHECKSUM_MANIFEST_COLUMNS)
    sips = patch_dict_list(join_dict_lists(transfer_manifests, checksum_manifests, "path"), "path", "path",lambda x: 'https://sbnarchive.psi.edu/pds4/surveys/gbo.ast.catalina.survey/' + x)
    
    with open(args.sip, "w") as f:
        f.writelines(format_sip_entry(sip) for sip in sips)


def format_sip_entry(sip):
    print(sip)
    return f'{sip["checksum"]}\tMD5\t{sip["path"]}\t{sip["lidvid"]}\r\n'


if __name__ == '__main__':
    sys.exit(main())