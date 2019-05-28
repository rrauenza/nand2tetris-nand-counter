#!/usr/bin/env python
import argparse
import logging
import os
import sys
import re
import lark

from collections import defaultdict

_SCRIPT_NAME = os.path.splitext(os.path.basename(sys.argv[0]))[0]

_GRAMMAR = r"""
    start: "CHIP" chipname "{" "IN" inblock+ "OUT" outblock+ "PARTS" ":" partsblock+ "}"

    assign: SYMBOL [RANGE] "=" SYMBOL [RANGE]
    assignments: assign ("," assign)*
    partsblock : partname "(" assignments ")" ";"

    inblock: SYMBOL [RANGE] ("," SYMBOL [RANGE])* ";"

    outblock: SYMBOL [RANGE] ("," SYMBOL [RANGE])* ";"
    chipname: SYMBOL
    partname: SYMBOL

    RANGE: "[" NUMBER ".." NUMBER "]" | "[" NUMBER "]"
    SYMBOL: /[a-zA-Z0-9]+/

    %import common.WS
    %import common.NUMBER
    %ignore WS
"""

_COUNTS = { "Nand": 1 }

def _main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+')
    args = parser.parse_args()
    ret = doit(args.files)
    sys.exit(ret)

def doit(files):
    all_chips = { 'Nand': [] }
    for f in files:
        with open(f, 'r') as fd:
            tree = parse_file(fd)
            chips = process_tree(tree)
            for chip, sub in chips.items():
                assert chip not in all_chips
                all_chips[chip] = sub

    for chipname in all_chips.keys():
        count = count_chip(all_chips, chipname)
        print "%s: %s" % (chipname, count)

def count_chip(chips, chipname):
    if chipname in _COUNTS:
        return _COUNTS[chipname]
    count = 0
    for chip in chips[chipname]:
        count += count_chip(chips, chip)
    _COUNTS[chipname] = count
    return count

def process_tree(tree):
    chips = defaultdict(list)
    chipname = None
    for node in tree.iter_subtrees():
        if node.data == 'chipname':
            assert node.children[0].type == 'SYMBOL'
            chipname = node.children[0].value
            # print "CHIP: %s" % chipname
        elif node.data == 'partname':
            assert node.children[0].type == 'SYMBOL'
            partname = node.children[0].value
            # print "    PART: %s" % partname
            chips[chipname].append(partname)
    return chips

def parse_file(fd):
    text = read_without_comments(fd)
    parser = lark.Lark(_GRAMMAR, parser='lalr', lexer='standard')
    tree = parser.parse(text)
    return tree

def read_without_comments(fd):
    text = fd.read()
    text = re.sub(r'//.*$', '', text, flags=re.M)
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
    return text

if __name__ == '__main__':
    try:
        sys.exit(_main(sys.argv[1:]))
    except KeyboardInterrupt:
        print >> sys.stderr, '%s: interrupted' % _SCRIPT_NAME
        sys.exit(130)
