# coding=utf8

import os
import pathlib

from ebook import make_ebook


def test_epub():
    path = pathlib.Path(__file__).resolve().parent.parent / 'examples'
    src = path / 'source'
    dst = path
    epub = make_ebook(str(src), str(dst), format="epub")
    assert os.path.isfile(epub)

    os.remove(epub)


def test_mobi():
    path = pathlib.Path(__file__).resolve().parent.parent / 'examples'
    src = path / 'source'
    dst = path
    mobi = make_ebook(str(src), str(dst), format="mobi")
    assert os.path.isfile(mobi)

    os.remove(mobi)
