#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
from hardcodes import search


parser = argparse.ArgumentParser()
parser.add_argument('-r', '--recursive', help='use post method', dest='recursive', action='store_true')
parser.add_argument('-c', '--comments', help='specify how to handles comments.\n\t\'ignore\'- ignore them\n\'parse\'- parse them like code\n\'string\'-return comments as hardcoded strings', dest='comments', default='parse')
parser.add_argument('-l', '--language', help='specify programming language of source code', dest='lang', default='common')
parser.add_argument('-o', help='don\'t show location of found strings', dest='hide_path', action='store_true')
parser.add_argument('-d', help='ignore directories. Example: tests,vendor,.git,one/two', default='', dest='ignore_dirs')
parser.add_argument('file', help='file', type=str)
args = parser.parse_args()


ignore_dirs = []
if args.ignore_dirs and os.path.isdir(args.file):
    idirs = args.ignore_dirs.split(',')
    for ids in idirs:
        ignore_dirs.append(os.path.join(args.file, ids))

files = []
if args.recursive:
    for root, dirs, l_files in os.walk(args.file):
        for file in l_files:

            check = True
            for ig in ignore_dirs:
                if ig in root:
                    check = False
            
            if check:
                files.append(os.path.join(root, file))
elif args.file:
    files.append(args.file)

for file in files:
    with open(file, 'r', encoding='utf-8') as code:
        try:
            code = '\n'.join([line for line in code])
        except UnicodeDecodeError:
            continue

    all_strings = search(code, args.lang, args.comments)
    if args.hide_path:
        prefix = ''
    else:
        prefix = file+':'
    for string in all_strings:
        print(prefix+string)
