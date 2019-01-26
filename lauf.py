#!/usr/bin/env python3
"""
    This is python2 + python3 compatible and has no third
    party dependencies.
"""

import sys
import time
import os
import pwd
import grp
from hashlib import md5
import json

from ipdb import set_trace

target_dir = ""
output_file = ""
blacklist_dirs = [
        "/tmp/",
        "/proc/",
        "/run/",
        "/dev/",
        "/sys/",
        "/lost+found",
        "/usr/share/man/",
        "/usr/include/",
]

counter_files = counter_dirs = 0

big_data = {}
errors = []


def parse_args():
    global target_dir, output_file
    if len(sys.argv) != 3:
        print("ERROR: {} <output file abs> <root dir>".format(sys.argv[0]))
        sys.exit(1)
    output_file = sys.argv[1]
    target_dir = sys.argv[2]


def get_perm(path):
    global errors
    file_info = {}
    file_info['type'] = 'dir'
    try:
        s = os.stat(path)
        file_info['owner'] = pwd.getpwuid(s.st_uid).pw_name
        file_info['group'] = grp.getgrgid(s.st_gid).gr_name
        file_info['permissions'] = oct(s.st_mode)[-4:]
    except (KeyError, OSError) as e:
        msg = "{}: {}".format(path, e)
        errors.append(msg)
    return file_info


def process_file(f_abs):
    file_info = get_perm(f_abs)
    file_info['type'] = 'file'  # get_perm sets fix dir. we overwrite here
    file_info['can_read'] = True
    try:
        with open(f_abs, "rb") as f:
            m = md5(f.read())
        file_info['md5'] = m.hexdigest()
    except Exception:
        file_info['can_read'] = False
    return file_info


def extract_files_and_dirs(target_dir):
    global counter_dirs, counter_files, big_data
    for dirpath, directories, filenames in os.walk(target_dir):

        # process all files
        for f in filenames:
            f_abs = os.path.join(dirpath, f)
            if is_blacklisted(f_abs):
                continue
            counter_files += 1
            print("FILE {}".format(f_abs))
            file_info = process_file(f_abs)
            big_data[f_abs] = file_info

        # process all dirs
        for d in directories:
            d_abs = os.path.join(dirpath, d)
            if is_blacklisted(d_abs):
                continue
            counter_dirs += 1
            print("DIR {}".format(d_abs))
            file_info = get_perm(d_abs)
            big_data[d_abs] = file_info
    print("\nProcessed {} files and {} dirs from {}".format(counter_files, 
                                                            counter_dirs,
                                                            target_dir))


def is_blacklisted(d_abs):
    for blacklisted_dir in blacklist_dirs:
        if d_abs.startswith(blacklisted_dir):
            print("BLACKLIST {}".format(d_abs))
            return True
    return False


def dump():
    with open(output_file, "w") as f:
        json.dump(big_data, f)
    print("Data written to {}".format(output_file))


if __name__ == '__main__':
    parse_args()
    start = time.time()
    extract_files_and_dirs(target_dir)
    dump()
    end = time.time()
    print("We needed {} seconds".format(int(end-start)))
    if len(errors) > 0:
        print("\nWe got the following errors:")
        for error in errors:
            print(error)
