# coding=utf8

import os
import tempfile
import shutil

import pytest

from kindle_maker.ebook_maker import Ebook

headers = [
    {
        'title': 'title1',
        'play_order': 2,
        'next_headers': [{'title': 'title1.1', 'play_order': 3}]
    },
    {
        'title': 'title2',
        'next_headers': [],
        'play_order': 4
    },
]


@pytest.fixture(scope='module')
def ebook():
    return Ebook(tempfile.gettempdir())


def test_templates_exist():
    templates_dir = os.path.join(
        os.path.dirname(__file__), '../kindle_maker/templates')

    assert os.path.exists(templates_dir)
    assert 'opf.xml' in os.listdir(templates_dir)
    assert 'toc.xml' in os.listdir(templates_dir)
    assert 'toc.html' in os.listdir(templates_dir)


def test_render_toc_ncx(ebook):

    ebook.render_toc_ncx(headers)
    ncx_file = os.path.join(ebook.dest_dir, 'toc.ncx')
    assert os.path.exists(ncx_file)
    with open(ncx_file, 'r') as f:
        text = f.read()
    assert '<text>title1</text>' in text
    os.remove(ncx_file)


def test_render_toc_html(ebook):

    ebook.render_toc_html(headers)
    toc_file = os.path.join(ebook.dest_dir, 'toc.html')
    assert os.path.exists(toc_file)
    with open(toc_file, 'r') as f:
        text = f.read()
    assert 'title1' in text
    os.remove(toc_file)


def test_render_opf(ebook):

    title = 'hello'
    ebook.render_opf(headers, title)
    opf_file = os.path.join(ebook.dest_dir, '%s.opf' % title)
    assert os.path.exists(opf_file)
    with open(opf_file, 'r') as f:
        text = f.read()
    assert 'title1' in text
    os.remove(opf_file)


def test_parse_headers(ebook):

    toc_md = os.path.join(ebook.dest_dir, 'toc.md')
    with open(toc_md, 'w') as f:
        f.writelines([
            'this is title\n',
            '# header1\n',
            '## header1.1\n'
        ])
    title, hs = ebook.parse_headers(toc_md)
    assert title == 'this is title'
    assert hs[0]['title'] == 'header1'
    os.remove(toc_md)
