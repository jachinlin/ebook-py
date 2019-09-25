# coding=utf8

import os

from kindle_maker import make_mobi


def test_make_ebook():
    src = './examples/source'
    dst = './examples/'
    mobi = make_mobi(src, dst)
    assert os.path.isfile(mobi)

    os.remove(mobi)