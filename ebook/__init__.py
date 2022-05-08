# coding=utf8

import sys
import os
import io

from ebook.ebooklib import Ebook


def make_epub():
    args = sys.argv[1:]
    if len(args) < 2:
        print("""make_epub usage:
1. prepare html files and a toc.md file in a source dir, and then call 
2. make_epub <source_dir> <output_dir>
        """)
        return

    make_ebook(args[0], args[1], "epub")

    print("success")


def make_mobi():
    args = sys.argv[1:]
    if len(args) < 2:
        print("""make_mobi usage:
1. prepare html files and a toc.md file in a source dir, and then call 
2. make_mobi <source_dir> <output_dir>
        """)
        return

    make_ebook(args[0], args[1], "mobi")

    print("success")


def _parse_headers(toc_file_name):
    """

    :param toc_file_name:
    :return:
    """
    if not os.path.isfile(toc_file_name):
        raise ValueError('toc.md file not exists:{}'.format(toc_file_name))

    headers_info = []

    with io.open(toc_file_name, mode='r', encoding='utf-8') as f:
        headers = f.readlines()
        if not headers:
            raise ValueError('invalid toc md file: title is empty')
        # first not empty line is tagged as title
        title_line = 0
        while not headers[title_line].strip() and title_line < len(headers):
            title_line += 1
        if title_line == len(headers):
            raise ValueError('invalid toc md file:  title is empty')
        title = headers[title_line].strip()

        # parse headings
        for h in headers[title_line + 1:]:
            if h.startswith('# '):
                headers_info.append({
                    'title': h[2:].strip(),
                    'next_headers': []
                })

            if h.startswith('## '):
                if len(headers) == 0:
                    sys.stderr.write('ignore heading: {}'.format(h))
                    continue
                headers_info[-1]['next_headers'].append({
                    'title': h[2:].strip(),
                })
        if not headers_info:
            raise ValueError('invalid toc md file: headings is empty')
    return title, headers_info


def make_ebook(source_dir: str, output_dir: str, format="epub") -> str:
    """
   make ebook with the files in source_dir and put the ebook made in output_dir
   :param source_dir:
   :param output_dir:
   :return: destination filename of the epub file
   """
    # parse toc.md file
    toc_file_name = os.path.join(source_dir, 'toc.md')
    title, headers = _parse_headers(toc_file_name)
    ebook = Ebook(title, source_folder=source_dir, ebook_format=format)
    cover = os.path.join(source_dir, 'cover.jpg')
    if os.path.isfile(cover):
        ebook.set_cover(cover_path=cover)
    for h in headers:
        c = ebook.create_chapter(
            h['title'],
            os.path.join(source_dir, '{}.html'.format(h['title']))
        )
        for sh in h['next_headers']:
            c.create_subchapter(
                sh['title'],
                os.path.join(source_dir, '{}.html'.format(sh['title']))
            )
    fn = os.path.join(output_dir, '{}.{}'.format(title, format))
    ebook.save_to(fn)
    return fn

