#!/usr/bin/env python3

import sys
import argparse
import typing

from dictops import patch_dict_list, dictify_file, index_dict_list

TRANSFER_MANIFEST_COLUMNS=['lidvid', 'slashpath']
CHECKSUM_MANIFEST_COLUMNS=['checksum', 'path']
SIP_COLUMNS=['checksum', 'method', 'url', 'lidvid']
NEW_CHECKSUM_COLUMNS=['checksum', 'path']

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sip", required=True)
    parser.add_argument("--checksum", required=True)
    parser.add_argument("--transfer", required=True)
    parser.add_argument("--new_checksums", required=True)

    args = parser.parse_args()

    new_checksums = dictify_file(args.new_checksums, NEW_CHECKSUM_COLUMNS)
    replacer = checksum_replacer(new_checksums, 'path', 'checksum')
    
    transfer_manifests = dictify_file(args.transfer, TRANSFER_MANIFEST_COLUMNS)
    transfer_manifests_with_path = patch_dict_list(transfer_manifests, "slashpath", "path", prefix_remover('/'))
    transfer_manifests_with_new_checksums = patch_dict_list(transfer_manifests_with_path, "checksum", "checksum", replacer)
    write_transformed(args.transfer + ".out", transfer_manifests_with_new_checksums, format_transfer_manifest_entry)
    
    checksum_manifests = dictify_file(args.checksum, CHECKSUM_MANIFEST_COLUMNS)
    checksum_manifests_with_new_checksums = patch_dict_list(checksum_manifests, "checksum", "checksum", replacer)
    write_transformed(args.checksum + ".out", checksum_manifests_with_new_checksums, format_checksum_manifest_entry)

    sips = dictify_file(args.sip, SIP_COLUMNS)
    sips_with_path = patch_dict_list(sips, "url", "path", prefix_remover('https://sbnarchive.psi.edu/pds4/surveys/gbo.ast.catalina.survey/'))
    sips_with_new_checksums = patch_dict_list(sips_with_path, "checksum", "checksum", replacer)
    write_transformed(args.sip + ".out", sips_with_new_checksums, format_sip_entry)


def write_transformed(dest_file: str, entry_list: typing.List[typing.Dict], func: typing.Callable) -> None:
    with open(dest_file, "w") as f:
        f.writelines(func(e) for e in entry_list)


def format_sip_entry(sip: typing.Dict) -> str:
    return f'{sip["checksum"]}\tMD5\t{sip["path"]}\t{sip["lidvid"]}\r\n'

def format_checksum_manifest_entry(e: typing.Dict) -> str:
    return ''

def format_transfer_manifest_entry(e: typing.Dict) -> str:
    return ''



def prefix_remover(prefix:str) -> str:
    prefixlen = len(prefix)
    def remove_prefix(val:str):
        if val.startswith(prefix):
            return val[prefixlen:]
        return val
    return remove_prefix

def checksum_replacer(new_checksum_dictlist: typing.List[typing.Dict], match_column: str, checksum_column: str) -> typing.Callable:
    checksum_index = index_dict_list(new_checksum_dictlist, match_column)
    def replace_checksum(path: str) -> str:
        return checksum_index[match_column][checksum_column] if path in checksum_index else None
    return replace_checksum

if __name__ == '__main__':
    sys.exit(main())