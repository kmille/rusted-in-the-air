#!/usr/bin/env python3

""" 
    Compares two outputs from lauf.py
"""

import sys
import json
from termcolor import colored, cprint

from ipdb import set_trace


blacklist = [
        '/etc/ssl/certs/',
        ]

j1 = j2 = j1_keys = j2_keys = None


def init():
    if len(sys.argv) != 3:
        print("{} <json1> <json2>".format(sys.argv[0]))
        sys.exit(1)
    load_files(sys.argv[1], sys.argv[2])


def load_files(file1, file2):
    global j1, j2, j1_keys, j2_keys
    with open(file1) as f:
        j1 = json.load(f)

    with open(file2) as f:
        j2 = json.load(f)

    j1_keys = j1.keys()
    j2_keys = j2.keys()


def is_blacklisted(f):
    for b in blacklist:
        if b in f:
            # print("BLACKLIST {}".format(f))
            return True
    return False


def compare(filename, f1, f2):
    properties = ['owner', 'group', 'permissions']
    for prop in properties:
        if f1[prop] != f2[prop]:
            print("MISMATCH {} {} {} {}".format(colored(prop, 'magenta'),
                                                f1[prop],
                                                f2[prop],
                                                colored(filename, 'magenta')))
    if f1['type'] == 'file':
        if f1['can_read'] and not f2['can_read']:
            print("MISMATCH file can only read in file1: {} {} {}".format(colored(filename, 'magenta'),
                                                                          f1['permissions'],
                                                                          f2['permissions']))
        if not f1['can_read'] and f2['can_read']:
            print("MISMATCH file can only read in file2: {} {} {}".format(colored(filename, 'magenta'),
                                                                          f1['permissions'],
                                                                          f2['permissions']))
        elif f1['can_read'] and f2['can_read']:
            if f1['md5'] != f2['md5']:
                print("MISMATCH {} {} {} {}".format(colored('md5', 'magenta'),
                                                    f1['md5'],
                                                    f2['md5'],
                                                    colored(filename, 'magenta')))


def go():
    cprint("Check if file from file1 is not in file2", 'green')
    for filename in j1_keys:
        if not is_blacklisted(filename) and filename not in j2.keys():
            print("NOT FOUND IN FILE2 {}".format(colored(filename, 'cyan')))

    cprint("Check if file from file2 is not in file1", 'green')
    for filename in j2_keys:
        if not is_blacklisted(filename) and filename not in j1.keys():
            print("NOT FOUND IN FILE1 {}".format(colored(filename, 'yellow')))

    cprint("Check if property of a file changed", 'green')
    for filename, file_info in j1.items():
        if not is_blacklisted(filename) and filename in j1_keys and filename in j2_keys:
            compare(filename, file_info, j2[filename])


if __name__ == '__main__':
    init()
    go()
