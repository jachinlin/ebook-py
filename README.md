# ebook-py

[![CI](https://github.com/jachinlin/ebook-py/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/jachinlin/ebook-py/actions/workflows/ci.yml)
[![Coverage Status](https://coveralls.io/repos/github/jachinlin/ebook-py/badge.svg)](https://coveralls.io/github/jachinlin/ebook-py)

ebook-py is a Python tool which, given a set of html files and a plain text file with toc information,
creates a MOBI file that you can directly use on your Amazon Kindle (or any other
device that supports MOBI documents).

Want to see what it looks like? Take a look at [examples](./examples)!


## Requirements

* A working Python 3 environment (tested on OS X + Python 3.7 + Virtualenv).

## Installation

1. (optional) Source your virtualenv.
2. `pip install git+https://github.com/jachinlin/ebook-py.git`

## Usage

1. prepare html files and a toc.md file in a source dir.
2. write a script

```
from kindle_maker import make_mobi

source_dir = 'put the source dir here'
output_dir = 'where you want to put the output mobi file'
make_mobi(source_dir, output_dir)

```

3. or call in a command-line tool

```
make_mobi <source_dir> <output_dir>
```
This will create a `<title>.mobi` in `<output dir>`. You can now transfer this
file to your device.

## Example

see examples at [examples](./examples).


## License

Have fun.
