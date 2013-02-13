cpath
=====

xpath search for c/c++ source code

usage
-----
usage: cpath.py [-h] [-x XPATH] file [file ...]

xpath search for c/c++ code

positional arguments:
  file                  c/c++ files to parse

optional arguments:
  -h, --help            show this help message and exit
  -x XPATH, --xpath XPATH
                        xpath query

examples
--------

find all binary operators using function pointers:
./cpath  -x '//type[@canonical_kind="FUNCTIONNOPROTO" or @canonical_kind="FUNCTIONPROTO"]/ancestor::type[@canonical_kind="POINTER"]/parent::UNEXPOSED_EXPR/parent::BINARY_OPERATOR[not(.//token/@spelling = "NULL") and not(.//token/@spelling = "=")]' example.c

