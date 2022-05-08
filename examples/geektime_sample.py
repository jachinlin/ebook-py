# coding=utf8

import pathlib

from ebook import Ebook


_chapters = [
    {
        'title': '技术领导力300讲',
        'file_path': '技术领导力300讲.html',
        'sections': [
            {
                'title': '卓越的团队必然有一个卓越的领导者',
                'file_path': '卓越的团队必然有一个卓越的领导者.html',
            },
            {
                'title': '你的能力模型决定你的职位',
                'file_path': '你的能力模型决定你的职位.html',
            },
            {
                'title': '从几个工程师到2000多个工程师的技术团队成长秘诀',
                'file_path': '从几个工程师到2000多个工程师的技术团队成长秘诀.html',
            },
            {
                'title': '从零开始搭建轻量级研发团队',
                'file_path': '从零开始搭建轻量级研发团队.html',
            },
        ]
    },
    {
        'title': '硅谷产品实战36讲',
        'file_path': '硅谷产品实战36讲.html',
        'sections': [
            {
                'title': '打造千万用户的世界级产品',
                'file_path': '打造千万用户的世界级产品.html',
            },
            {
                'title': '什么是优秀的产品经理',
                'file_path': '什么是优秀的产品经理.html',
            },
            {
                'title': '硅谷的产品经理是什么样子的',
                'file_path': '硅谷的产品经理是什么样子的.html',
            }
        ]
    }
]


def sample_ebook(format: str) -> str:
    title = '极客时间样章'

    source_folder = str(pathlib.Path(__file__).parent / 'source')
    ebook = Ebook(title, ebook_format=format, source_folder=source_folder)
    for c in _chapters:
        chapter = ebook.create_chapter(
            c['title'],
            c['file_path']
        )
        for s in c['sections']:
            chapter.create_subchapter(
                s['title'],
                s['file_path']
            )
    fn = '{}.{}'.format(title, format)
    ebook.save_to(fn)
    return fn


if __name__ == '__main__':
    sample_ebook(format='mobi')
    sample_ebook(format='epub')
