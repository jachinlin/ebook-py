# coding=utf8

import os

import pytest

from kindle_maker.ebooklib import Ebook, EbookUtil


@pytest.fixture(scope='module')
def ebook() -> Ebook:
    e = Ebook(title='Title Test')
    c = e.create_chapter('Chapter 1')
    c.set_content('<body>chapter1 xxxxx</body>')
    sc = c.create_subchapter('Session 1.1')
    sc.set_content('<body>session 1.1 xxx</body>')
    c2 = e.create_chapter('Chapter 2')
    c2.set_content('<body>chapter2 xxxxx</body>')
    return e


@pytest.fixture(scope='module')
def eu(ebook) -> EbookUtil:
    return EbookUtil(ebook)


def test_templates_exist():
    templates_dir = os.path.join(
        os.path.dirname(__file__), '../kindle_maker/templates')

    assert os.path.exists(templates_dir)
    assert 'opf.xml' in os.listdir(templates_dir)
    assert 'toc.xml' in os.listdir(templates_dir)
    assert 'toc.html' in os.listdir(templates_dir)


def test_render_toc_ncx(eu, ebook):

    ncx = eu._render_toc_ncx()
    ncx_file = ebook.tmpdir / ncx
    assert ncx_file.is_file()
    with ncx_file.open() as f:
        text = f.read()
    assert '<text>Title Test</text>' in text


def test_render_toc_html(eu, ebook):

    toc = eu._render_toc_html()
    toc_file = ebook.tmpdir / toc
    assert toc_file.is_file()
    with toc_file.open() as f:
        text = f.read()
    assert 'Chapter 1' in text


def test_render_opf(eu, ebook):

    opf = eu._render_opf()
    opf_file = ebook.tmpdir / opf
    assert opf_file.is_file()
    with opf_file.open() as f:
        text = f.read()
    assert 'Title Test' in text


# def test_ebook_show(ebook):
#     assert ebook.show() == 0


def test_ebook_save(ebook):
    f = 'test.mobi'
    ebook.save(f)
    assert os.path.isfile(f)
    os.remove(f)

