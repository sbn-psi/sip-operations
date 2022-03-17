import argparse
import hashlib
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dirname")
    parser.add_argument("--urlbase")
    args = parser.parse_args()
    for label in discover_labels(args.dirname):
        lidvid = extract_lidvid(label)
        files = build_file_list(label)

        generate_entries(files, args.urlbase)

def generate_entries(files, urlbase, lidvid):
    checksum = md5sum(file_path)
    url = f'{urlbase}/{file_path}'

    for file_path in files:
        print(gen_checksum_manifest_entry(checksum, file_path))
        print(gen_transfer_manifest_entry(lidvid, file_path))
        print(gen_sip_entry(checksum, url, lidvid))

def gen_checksum_manifest_entry(checksum, file_path):
    return f'{checksum}{file_path}'

def gen_transfer_manifest_entry(lidvid, file_path):
    return f'{lidvid}{file_path}'

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
    with open(file_path) as f:
        h.update(f.read())
        return h.hexdigest

if __name__ == '__main__':
    sys.exit(main())