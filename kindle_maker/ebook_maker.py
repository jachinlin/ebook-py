# coding=utf8

import io
import os
import sys
import datetime
import shutil
import tempfile
import subprocess

from jinja2 import Environment, FileSystemLoader

from kindle_maker.kindlegen import kindlegen

templates_env = Environment(loader=FileSystemLoader(
    '{}/templates/'.format(os.path.dirname(os.path.realpath(__file__)))))
_default_output_dir = os.path.join(tempfile.gettempdir(), 'kindle_maker')


class Ebook:

    def __init__(self, dest_dir):
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        self._dest_dir = dest_dir

    @property
    def dest_dir(self):
        return self._dest_dir

    def render_file(self, template_name, context, to_filename):
        template = templates_env.get_template(template_name)
        with io.open(os.path.join(self._dest_dir, to_filename),
                     mode="w", encoding='utf-8') as f:
            f.write(template.render(**context))

    def render_toc_ncx(self, headers, title=None, author=None):
        """

        :param headers:
        :param title:
        :param author:
        :return:
        """
        self.render_file(
            'toc.xml',
            {
                'headers': headers,
                'title': title or 'jachinlin.github.io' + str(datetime.date.today()),
                'author': author or 'jachinlin.github.io'
            },
            'toc.ncx'
        )

    def render_toc_html(self, headers):
        """

        :param headers:
        :return:
        """
        self.render_file('toc.html', {'headers': headers}, 'toc.html')

    def render_opf(self, headers, title, author=None):
        """

        :param headers:
        :param title:
        :param author:
        :return:
        """
        self.render_file(
            'opf.xml',
            {
                'headers': headers,
                'title': title,
                'author': author or 'jachinlin.github.io'
            },
            '{}.opf'.format(title)
        )

    @staticmethod
    def parse_headers(toc_file_name):
        """

        :param toc_file_name:
        :return:
        """
        if not os.path.isfile(toc_file_name):
            raise ValueError('toc.md file not exists:{}'.format(toc_file_name))

        headers_info = []

        with io.open(toc_file_name, mode='r', encoding='utf-8') as f:
            headers = f.readlines()
            order = 1
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
                    order += 1
                    headers_info.append({
                        'title': h[2:].strip(),
                        'play_order': order,
                        'next_headers': []
                    })

                if h.startswith('## '):
                    if len(headers) == 0:
                        sys.stderr.write('ignore heading: {}'.format(h))
                        continue
                    order += 1
                    headers_info[-1]['next_headers'].append({
                        'title': h[2:].strip(),
                        'play_order': order,
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
    output_dir = output_dir or _default_output_dir
    source_dir = os.path.abspath(os.path.expanduser(source_dir))
    output_dir = os.path.abspath(os.path.expanduser(output_dir))
    ebook = Ebook(source_dir)

    # parse toc.md file
    toc_file_name = os.path.join(source_dir, 'toc.md')
    title, headers = ebook.parse_headers(toc_file_name)

    # cover
    cover_file_name = os.path.join(source_dir, 'cover.jpg')
    if not os.path.isfile(cover_file_name):
        cover = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             'templates', 'cover.jpg')
        sys.stderr.write('use default cover.jpg')
        shutil.copy(cover, source_dir)

    # render toc.ncx file
    ebook.render_toc_ncx(headers)
    # render toc.html file
    ebook.render_toc_html(headers)
    # render opf file
    ebook.render_opf(headers, title)

    # make mobi ebook in source_dir
    opf_file = os.path.join(source_dir, title + '.opf')
    mobi_file = title + '.mobi'
    subprocess.call([kindlegen, '-dont_append_source', opf_file])
    # move mobi file to output dir
    dest = shutil.move(
        os.path.join(source_dir, mobi_file),
        os.path.join(output_dir, mobi_file)
    )

    return dest

