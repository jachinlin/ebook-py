#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='kindle_maker',
    version='0.0.1',
    author='jachinlin',
    author_email='linjx1000@gmail.com',
    url='https://github.com/jachinlin/kindle_maker',
    description='a tool make kindle mobi ebook',
    license='MIT',
    keywords='kindle ebook mobi',
    packages=['kindle_maker'],
    package_data={'kindle_maker': ['templates/*']},
    install_requires=[
        'Jinja2==2.10'
    ],
    entry_points={
        'console_scripts': [
            'make_mobi = kindle_maker:make_mobi_command',
        ],
    }
)
