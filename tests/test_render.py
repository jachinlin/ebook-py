# coding=utf8

import os
import tempfile
from kindle_maker.ebook_maker import render_toc_ncx, render_toc_html, render_opf, parse_headers

headers = [
    {'title': 'title1', 'play_order': 2, 'next_headers': [{'title': 'title1.1', 'play_order': 3}]},
    {'title': 'title2', 'next_headers': [], 'play_order': 4},
]


def test_templates_exist():
    templates_dir = os.path.join(os.path.dirname(__file__), '../kindle_maker/templates')

    assert os.path.exists(templates_dir)
    assert 'opf.xml' in os.listdir(templates_dir)
    assert 'toc.xml' in os.listdir(templates_dir)
    assert 'toc.html' in os.listdir(templates_dir)


def test_render_toc_ncx():
    directory = os.path.join(tempfile.gettempdir(), 'kindle_maker')
    if not os.path.exists(directory):
        os.makedirs(directory)
    render_toc_ncx(headers, directory)
    ncx_file = os.path.join(directory, 'toc.ncx')
    assert os.path.exists(ncx_file)

    with open(ncx_file, 'r') as f:
        text = f.read()

    assert '<text>title1</text>' in text

    os.system('rm %s' % ncx_file)


def test_render_toc_html():
    directory = os.path.join(tempfile.gettempdir(), 'kindle_maker')
    if not os.path.exists(directory):
        os.makedirs(directory)
    render_toc_html(headers, directory)
    toc_file = os.path.join(directory, 'toc.html')
    assert os.path.exists(toc_file)

    with open(toc_file, 'r') as f:
        text = f.read()

    assert 'title1' in text

    os.system('rm %s' % toc_file)


def test_render_opf():
    directory = os.path.join(tempfile.gettempdir(), 'kindle_maker')
    if not os.path.exists(directory):
        os.makedirs(directory)
    title = 'hello'
    render_opf(headers, title, directory)
    opf_file = os.path.join(directory, '%s.opf' % title)
    assert os.path.exists(opf_file)

    with open(opf_file, 'r') as f:
        text = f.read()

    assert 'title1' in text

    os.system('rm %s' % opf_file)


def test_parse_headers():
    directory = os.path.join(tempfile.gettempdir(), 'kindle_maker')
    if not os.path.exists(directory):
        os.makedirs(directory)
    _file = os.path.join(directory, 'toc.md')
    with open(_file, 'w') as f:
        f.writelines([
            'this is title\n',
            '# header1\n',
            '## header1.1\n'
        ])

    title, hs = parse_headers(_file)

    assert title == 'this is title'
    assert hs[0]['title'] == 'header1'
    os.system('rm %s' % _file)
