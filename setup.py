#!/usr/bin/env python
# coding=utf-8


from setuptools import setup

version = '1.0.0'

setup(
    name='kindle_maker',
    version=version,
    author='jachinlin',
    author_email='linjx1000@gmail.com',
    url='https://github.com/jachinlin/kindle_maker',
    description='a tool make kindle mobi ebook',
    license='MIT',
    keywords='kindle ebook mobi',
    packages=['kindle_maker'],
    package_data={'kindle_maker': [
        'templates/*',
        'bin/linux/kindlegen',
        'bin/mac/kindlegen'
    ]},
    install_requires=[
        'Jinja2'
    ],
    entry_points={
        'console_scripts': [
            'make_mobi=kindle_maker:make_mobi_command',
        ],
    }
)
