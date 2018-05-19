# Kindle ebook making

[![travis](https://api.travis-ci.org/jachinlin/kindle_maker.svg?branch=master)](https://travis-ci.org/jachinlin/kindle_maker)
[![codecov](https://codecov.io/gh/jachinlin/kindle_maker/branch/master/graph/badge.svg)](https://codecov.io/gh/jachinlin/kindle_maker)


kindle_maker is a Python tool which, given a set of html files and a plain text file with toc message,
creates a MOBI file that you can directly use on you Amazon Kindle (or any other
device that supports MOBI documents).

Want to see what it looks like? Take a look at `examples/!


## Requirements

* A working Python 3 environment (tested on OS X + Python 3.5 + Virtualenv).
* [Amazon's KindleGen](https://www.amazon.com/gp/feature.html?ie=UTF8&docId=1000765211)
  binary.

## Installation

1. (optional) Source your virtualenv.
2. `pip install git+https://github.com/jachinlin/kindle_maker.git`

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

see examples at `examples`!


## License

Have fun.
