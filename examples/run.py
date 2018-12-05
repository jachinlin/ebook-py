# coding=utf8
import sys
sys.path.append('.')
from kindle_maker.ebook_maker import make_ebook

if __name__ == '__main__':
    make_ebook('./examples/source', '.')
