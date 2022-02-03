#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, re
import argparse
from hardcodes import search


parser = argparse.ArgumentParser()
parser.add_argument('-r', '--recursive', help='use post method', dest='recursive', action='store_true')
parser.add_argument('-c', '--comments', help='specify how to handles comments.\n\t\'ignore\'- ignore them\n\'parse\'- parse them like code\n\'string\'-return comments as hardcoded strings', dest='comments', default='parse')
parser.add_argument('-l', '--language', help='specify programming language of source code', dest='lang', default='common')
parser.add_argument('-n', '--line-numbers', help='include source code line numbers in output', action='store_true')
parser.add_argument('-q', "--query", help='extract only strings matchng the regex', dest='query_match', default='')
parser.add_argument('-o', help='don\'t show location of found strings', dest='hide_path', action='store_true')
parser.add_argument('file', help='file', type=str)
args = parser.parse_args()

files = []
show_line_numbers:bool = args.line_numbers

if args.recursive:
    for root, dirs, l_files in os.walk(args.file):
      for file in l_files:
        files.append(os.path.join(root, file))
elif args.file:
    files.append(args.file)

for file in files:
    # with open(file, 'r', encoding='utf-8') as code:
    with open(file, 'r') as code:
        try:
            # code = '\n'.join([(line.strip()) for line in code])
            code = '\n'.join([re.sub('\n', '', line) for line in code])
        except UnicodeDecodeError:
            continue

    all_strings = search(code, args.lang, args.comments, show_line_numbers, args.query_match)
    
    if args.hide_path:
        prefix = ''
    else:
        prefix = file+':'
        
    for string in all_strings:
        print(prefix+string)
