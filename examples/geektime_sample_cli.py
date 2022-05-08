# coding=utf8

import pathlib

from ebook import make_ebook

if __name__ == '__main__':
    src_folder = pathlib.Path(__file__).resolve().parent / 'source'
    make_ebook(str(src_folder), '.', format='mobi')
    make_ebook(str(src_folder), '.', format='epub')
