#!/usr/bin/env python3

import argparse
import sys
import os.path
import tempfile
import shutil
import re
import functools


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sip", required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--dest", required=True)

    args = parser.parse_args()

    label = readfile(args.label)
    filesize, linecount = get_stats(args.sip)
    replacements = {
        "file_size": filesize,
        "object_length": filesize,
        "records": linecount
    }
    funcs = [functools.partial(replace_element, k, v) for (k,v) in replacements.items()]
    newlabel = functools.reduce(lambda x,f: f(x), funcs, label)

    output_path = os.path.join(args.dest, os.path.basename(args.label))
    with open(output_path, "w") as out:
        out.write(newlabel)

    return 0

def replace_element(element_name, value, str):
    pattern = f"<{element_name}(.*)>.*</{element_name}>"
    print (pattern)
    replacement = f"<{element_name}\\1>{value}</{element_name}>"
    print (replacement)
    return re.sub(pattern, replacement, str)

def readfile(filename):
    with open(filename) as f:
        return f.read()

def replacefile(filename, contents):
    _, output_path = tempfile.mkstemp()
    with open(output_path, "w") as out:
        out.write(contents)
    
    if os.path.exists(filename):
        shutil.move(filename, filename + ".bak")
    shutil.move(output_path, filename)

def get_stats(filepath):
    filesize = os.path.getsize(filepath)
    linecount = sum(1 for x in open(filepath))
    return filesize, linecount



if __name__ == '__main__':
    sys.exit(main())
