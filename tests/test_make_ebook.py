# coding=utf8

import os
import pathlib

from kindle_maker import make_mobi


def test_make_ebook():
    path = pathlib.Path(__file__).parent.parent / 'examples'
    src = str(path / 'source')
    dst = str(path)
    mobi = make_mobi(src, dst)
    assert os.path.isfile(mobi)

    os.remove(mobi)
