# -*- coding: utf-8 -*-

import tempfile
import pathlib
import time
import shutil
import platform
import os
import subprocess
import io
import sys
import warnings
from typing import Optional, List

from jinja2 import Environment, FileSystemLoader

from kindle_maker.kindlegen import kindlegen


def format_file_name(path: str) -> str:
    """
    strip illegal characters
    """
    return path.replace('/', '').replace(' ', ''). \
        replace('+', '-').replace('"', '').replace('\\', ''). \
        replace(':', '-').replace('|', '-')


class EbookUtil:

    def __init__(self, ebook: 'Ebook'):
        self._templates_env = Environment(loader=FileSystemLoader(
            str(pathlib.Path(__file__).parent / 'templates/')))
        self._ebook = ebook
        self._headings = None

    @property
    def headings(self) -> List[dict]:
        """
        {
            'title': 'xxx',
            'play_order': xxx,
            'file_name': 'xxxx',
            'sub_headings': List[headings]
        }
        """
        if self._headings:
            return self._headings
        hs = list()
        order = 1
        for c in self._ebook.chapter_list:
            order += 1
            h = dict(title=c.title, play_order=order,
                     file_name=str(c.dest_file_path), sub_headings=[])
            for sc in c.sub_chapters:
                order += 1
                h['sub_headings'].append(dict(title=sc.title,
                                              play_order=order,
                                              file_name=str(sc.dest_file_path)))
            hs.append(h)
        self._headings = hs
        return hs

    def _render_file(self, template_name: str, context: dict, to_filename: str):
        template = self._templates_env.get_template(template_name)
        with (self._ebook.tmpdir / to_filename).open(
                mode="w", encoding='utf-8') as f:
            f.write(template.render(**context))

    def _render_toc_ncx(self):
        ncx = 'toc.ncx'
        self._render_file(
            'toc.xml',
            {
                'headings': self.headings,
                'title': self._ebook.title,
                'author': self._ebook.author or 'jachinlin.github.io'
            },
            ncx
        )
        return ncx

    def _render_toc_html(self):
        toc = 'toc.html'
        self._render_file(toc, {'headings': self.headings}, toc)
        return toc

    def _render_opf(self) -> str:
        opf_file = '{}.opf'.format(format_file_name(self._ebook.title))
        self._render_file(
            'opf.xml',
            {
                'headings': self.headings,
                'title': self._ebook.title,
                'author': self._ebook.author or 'jachinlin.github.io'
            },
            opf_file
        )
        return opf_file

    def _save_cover(self) -> None:
        if self._ebook.cover_path:
            cover_path = self._ebook.cover_path
            shutil.copy(cover_path, str(self._ebook.tmpdir))
        elif self._ebook.cover_content:
            raise NotImplementedError
        else:
            cover = pathlib.Path(__file__).parent / 'templates/cover.jpg'
            shutil.copy(str(cover), str(self._ebook.tmpdir))

    def _save_chapters(self) -> None:
        for c in self._ebook.chapter_list:
            c.save()
            for sc in c.sub_chapters:
                sc.save()

    def create(self):
        self._render_toc_ncx()
        self._render_toc_html()
        opf_file = self._render_opf()
        self._save_cover()
        self._save_chapters()
        rc = subprocess.call([
            kindlegen, '-dont_append_source', str(self._ebook.tmpdir / opf_file)
        ])
        if rc != 0:
            pass
            # raise Exception('kindlegen failed')


class Chapter:
    max_level = 2

    def __init__(self, title: str, ebook: 'Ebook',
                 file_path: str = None, level: int = 1):
        self.title = title
        self._ebook = ebook
        if file_path and not pathlib.Path(file_path).is_file():
            raise ValueError('{} is not a file'.format(file_path))
        self._file_path = file_path
        self._level = level
        self._content = Optional[None]
        self._static_files = list()
        self.sub_chapters = list()

    @property
    def dest_file_path(self) -> pathlib.Path:
        return pathlib.Path('{}.html'.format(format_file_name(self.title)))

    @property
    def full_dest_file_path(self) -> pathlib.Path:
        return self._ebook.tmpdir / self.dest_file_path

    @property
    def content(self) -> str:
        if self._file_path:
            return io.open(self._file_path, encoding='utf-8').read()
        return self._content

    @property
    def is_top_chapter(self):
        return self._level == 1

    def set_content(self, content: str) -> 'Chapter':
        self._content = content
        self._file_path = None
        return self

    def add_static_files(self, *file_path) -> 'Chapter':
        for f in file_path:
            assert pathlib.Path(f).is_file(), '{} is not a file'.format(f)
        self._static_files.extend(file_path)
        return self

    def create_subchapter(self, chapter_title: str,
                          chapter_file_path: str = None) -> 'Chapter':
        if self._level >= self.max_level:
            raise Exception('chapter level is great than '
                            'the max level num: {}'.format(self.max_level))

        ct = Chapter(chapter_title, self._ebook,
                     chapter_file_path, level=self._level + 1)
        self.sub_chapters.append(ct)
        return ct

    def save(self):
        dest_file_path = self.full_dest_file_path
        with dest_file_path.open(mode='w', encoding='utf-8') as f:
            f.write(self.content)
        for f in self._static_files:
            shutil.copy(f, str(dest_file_path.parent))


class Ebook:

    def __init__(self, title: str, author=None):
        self.title = title
        self.author = author
        self.cover_path = None
        self.cover_content = None
        self._tempdir = pathlib.Path(tempfile.gettempdir()) / str(time.time())
        self._tempdir.mkdir()
        self.chapter_list = list()
        self._eu = EbookUtil(self)

    @property
    def dest_file_path(self) -> pathlib.Path:
        return pathlib.Path('{}.mobi'.format(format_file_name(self.title)))

    @property
    def full_dest_file_path(self) -> pathlib.Path:
        return self.tmpdir / self.dest_file_path

    @property
    def tmpdir(self) -> pathlib.Path:
        return self._tempdir

    def set_cover(self, cover_path: str = None,
                  cover_content: bytes = None) -> 'Ebook':
        if cover_path:
            self.cover_path = cover_path
            self.cover_content = None
            return self
        if cover_content:
            self.cover_content = cover_content
            self.cover_path = None
            return self
        raise ValueError('img_path and img_content are both empty')

    def add_chapter(self, chapter: Chapter) -> 'Ebook':
        if not chapter.is_top_chapter:
            raise ValueError('only chapters with level 1 are accepted')
        self.chapter_list.append(chapter)
        return self

    def create_chapter(self, chapter_title: str,
                       chapter_file_path: str = None) -> Chapter:
        """
        create a chapter
        """
        ct = Chapter(chapter_title, self, chapter_file_path)
        self.add_chapter(ct)
        return ct

    def _create(self):
        if not self.chapter_list:
            raise ValueError('chapter list is empty')
        return self._eu.create()

    def save(self, file_path: str):
        """
        create the ebook and save to the given file_path
        """
        self._create()
        shutil.copy(str(self.tmpdir / self.dest_file_path), file_path)

    def show(self) -> int:
        """
        show the ebook with the default viewer
        """
        self._create()
        system = platform.system()
        if system == 'Linux':
            return subprocess.call(['xdg-open', str(self.full_dest_file_path)])
        elif system == 'Darwin':
            return subprocess.call(['open', str(self.full_dest_file_path)])
        else:
            return os.startfile(str(self.full_dest_file_path))

    def __del__(self):
        """
        remove the temp files after all things done
        """
        def rmtree(root):
            for p in root.iterdir():
                if p.is_dir():
                    rmtree(p)
                else:
                    p.unlink()
            root.rmdir()
        rmtree(self.tmpdir)


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


def make_ebook(source_dir, output_dir=None):
    """
    make ebook with the files in source_dir and put the ebook made in output_dir
    :param source_dir:
    :param output_dir:
    :return: destination filename of the mobi file
    """
    warnings.warn(
        '``make_ebook`` api is deprecated, and use ``Ebook`` class instead!')
    # parse toc.md file
    toc_file_name = os.path.join(source_dir, 'toc.md')
    title, headers = _parse_headers(toc_file_name)
    ebook = Ebook(title)
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
    src_files = os.listdir(source_dir)
    for fn in src_files:
        full_fn = os.path.join(source_dir, fn)
        if os.path.isfile(full_fn) and not fn.endswith('html'):
            shutil.copy(full_fn, str(ebook.tmpdir))
    fn = os.path.join(output_dir, '{}.mobi'.format(title))
    ebook.save(fn)
    return fn

