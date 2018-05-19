# coding=utf8

import sys
from .ebook_maker import make_ebook as make_mobi


def make_mobi_command():
    args = sys.argv[1:]
    if len(args) < 2:
        print("""make_mobi usage:
1. prepare html files and a toc.md file in a source dir, and then call 
2. make_mobi <source_dir> <output_dir>
        """)
        return

    make_mobi(args[0], args[1])

    print("success")
