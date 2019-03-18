#!/usr/bin/env python3

import os
import sys

from sqlitedict import SqliteDict


def argparser():
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('dbname', help='name of database to create')
    ap.add_argument('file', nargs='+', help='files to insert')
    return ap
        

def main(argv):
    args = argparser().parse_args(argv[1:])
    with SqliteDict(args.dbname, autocommit=True) as db:
        for fn in args.file:
            bn = os.path.basename(fn)
            db[bn] = open(fn).read()
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
