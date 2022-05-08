#!/usr/bin/env python
# coding=utf-8


from setuptools import setup
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel


class bdist_wheel(_bdist_wheel):

    def finalize_options(self):
        _bdist_wheel.finalize_options(self)
        self.root_is_pure = False

    def get_tag(self):
        python, abi, plat = _bdist_wheel.get_tag(self)
        # We don't contain any python source
        python, abi = 'py2.py3', 'none'
        return python, abi, plat


version = '1.1.0'

setup(
    name='ebook',
    version=version,
    author='jachinlin',
    author_email='linjx1000@gmail.com',
    url='https://github.com/jachinlin/ebook-py',
    description='ebook tool',
    license='MIT',
    keywords='kindle ebook mobi epub',
    packages=['ebook'],
    package_data={'ebook': [
        'templates/*',
        'bin/linux/kindlegen',
        'bin/mac/kindlegen'
    ]},
    install_requires=[
        'Jinja2'
    ],
    entry_points={
        'console_scripts': [
            'make_epub=ebook:make_epub',
            'make_mobi=ebook:make_mobi',
        ],
    },
    cmdclass={'bdist_wheel': bdist_wheel}
)
