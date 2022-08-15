#!/usr/bin/env mayapy

import sphinx
import sys
import os

if __name__ == '__main__':
    argv = sys.argv[1:]
    cwd = os.getcwd()
    argv.insert(0, sphinx.__file__)
    sphinx.main(argv)
