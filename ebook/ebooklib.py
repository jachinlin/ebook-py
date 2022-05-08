# -*- coding: utf-8 -*-
import datetime
import pathlib
import shutil
import platform
import os
import subprocess
import re
import zipfile
from typing import Optional, List

from jinja2 import Environment, FileSystemLoader

from ebook.kindlegen import kindlegen


class FolderNotFoundError(OSError):
    """ folder not found. """


def format_file_name(path: str) -> str:
    """
    remove illegal characters
    """
    return re.sub(r'[/\\?%*:|"\'<>.,;=\s+]+', '', path)


class EbookUtil:

    def __init__(self, ebook: 'Ebook'):
        self._templates_env = Environment(loader=FileSystemLoader(
            str(pathlib.Path(__file__).parent / 'templates/')))
        self._ebook = ebook
        self._headings = None

    @property
    def headings(self) -> List[dict]:
        """
        generate the ebook headings

        dict format
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
                     file_name=str(c.file_path), sub_headings=[])
            for sc in c.sub_chapters:
                order += 1
                h['sub_headings'].append(dict(title=sc.title,
                                              play_order=order,
                                              file_name=str(sc.file_path)))
            hs.append(h)
        self._headings = hs
        return hs

    def _render_file(self, template_name: str, context: dict, to_filename: str):
        template = self._templates_env.get_template(template_name)
        with (self._ebook.work_folder / to_filename).open(
                mode="w", encoding='utf-8') as f:
            f.write(template.render(**context))

    def _render_container_xml(self) -> str:
        container = 'container.xml'
        self._render_file('container.xml', {}, container)
        return container

    def _render_toc_ncx(self) -> str:
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

    def _render_toc_html(self) -> str:
        toc = 'toc.html'
        self._render_file(toc, {'headings': self.headings}, toc)
        return toc

    def _render_opf(self) -> str:
        opf = 'content.opf'
        self._render_file(
            'opf.xml',
            {
                'headings': self.headings,
                'title': self._ebook.title,
                'author': self._ebook.author or 'jachinlin.github.io'
            },
            opf
        )
        return opf

    def _save_cover(self) -> None:
        if self._ebook.cover_path:
            cover_path = self._ebook.cover_path
            shutil.copy(cover_path, str(self._ebook.work_folder))
        else:
            # default cover
            cover = pathlib.Path(__file__).parent / 'templates/cover.jpg'
            shutil.copy(str(cover), str(self._ebook.work_folder))

    def _move_source_files(self) -> None:
        src_files = os.listdir(self._ebook.source_folder)
        for fn in src_files:
            full_fn = os.path.join(self._ebook.source_folder, fn)
            if os.path.isfile(full_fn):
                shutil.copy(full_fn, self._ebook.work_folder)

    def _generate_all_files(self):
        """
        generate all files
        """
        self._render_container_xml()
        self._render_toc_ncx()
        self._render_toc_html()
        opf_file = self._render_opf()
        self._save_cover()
        self._move_source_files()

        mimetype_fn = str(self._ebook.work_folder / 'mimetype')
        with open(mimetype_fn, 'w') as f:
            f.write('application/epub+zip')

    def _create_mobi(self, file_path: pathlib.Path):
        """
        create a mobi ebook
        """
        self._generate_all_files()
        fn = file_path.name
        rc = subprocess.call([
            kindlegen, '-dont_append_source', str(self._ebook.work_folder / 'content.opf'), '-o', fn
        ])
        if rc != 0:
            pass
            # raise Exception('kindlegen failed')
        shutil.copy(self._ebook.work_folder / fn, file_path)

    def _create_epub(self, file_path: pathlib.Path):
        """
        create a epub ebook
        """
        self._generate_all_files()
        wf = self._ebook.work_folder

        with zipfile.ZipFile(file_path, 'w') as zipf:
            zipf.write(str(wf / 'mimetype'), 'mimetype', compress_type=zipfile.ZIP_STORED)
            for file in wf.rglob('*.*'):
                zipf.write(
                    str(file), str(file.relative_to(wf)),
                    compress_type=zipfile.ZIP_DEFLATED
                )

    def create(self, file_path: pathlib.Path):
        getattr(self, '_create_{}'.format(self._ebook.format))(file_path)


class Chapter:
    max_level = 2

    def __init__(self, title: str, ebook: 'Ebook',
                 file_path: str, level: int = 1):
        self.title = title
        self._ebook = ebook
        if not (self._ebook.source_folder / file_path).is_file():
            raise FileNotFoundError('{} not found'.format(file_path))
        self.file_path = file_path
        self._level = level
        self.sub_chapters: List['Chapter'] = list()

    @property
    def is_top_chapter(self):
        return self._level == 1

    def create_subchapter(self, chapter_title: str,
                          chapter_file_path: str = None) -> 'Chapter':
        if self._level >= self.max_level:
            raise Exception('chapter level is great than '
                            'the max level num: {}'.format(self.max_level))
        ct = Chapter(chapter_title, self._ebook,
                     chapter_file_path, level=self._level + 1)
        self.sub_chapters.append(ct)
        return ct


class Ebook:

    def __init__(self, title: str, source_folder: str, author=None, ebook_format: str = 'mobi'):
        self.title: str = title
        self.format = ebook_format
        self.author: str = author
        self.cover_path: Optional[str] = None
        self.chapter_list = list()
        sf = pathlib.Path(source_folder)
        if not sf.is_dir():
            raise FolderNotFoundError('{} not found'.format(source_folder))
        self.source_folder = sf
        self.work_folder = self.source_folder / ".{}.{}".format(format_file_name(self.title), datetime.datetime.now())
        self.work_folder.mkdir()
        self._eu = EbookUtil(self)

    def set_cover(self, cover_path: str) -> 'Ebook':
        if not pathlib.Path(cover_path).is_file():
            raise FileNotFoundError('{} not found'.format(cover_path))
        self.cover_path = cover_path
        return self

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

    def _create(self, file_path: pathlib.Path):
        if not self.chapter_list:
            raise ValueError('chapter list is empty')
        return self._eu.create(file_path)

    def save_to(self, file_path: str):
        """
        create the ebook and save to the given file_path
        """
        file_path = pathlib.Path(os.getcwd()) / file_path
        self._create(file_path)

    def show(self):
        """
        show the ebook with the default viewer
        """
        fn = pathlib.Path(os.getcwd()) / ".{}.{}".format(format_file_name(self.title), self.format)
        self._create(fn)
        if not fn.is_file():
            raise FileNotFoundError('{} not found'.format(fn))

        system = platform.system()
        if system == 'Linux':
            subprocess.call(['xdg-open', str(fn)])
        elif system == 'Darwin':
            subprocess.call(['open', str(fn)])
        else:
            os.startfile(str(fn))

    def __del__(self):
        """
        remove the temp files after all things done
        """
        shutil.rmtree(self.work_folder)
