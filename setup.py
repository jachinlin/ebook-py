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


version = '1.0.4'

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
    },
    cmdclass={'bdist_wheel': bdist_wheel}
)
