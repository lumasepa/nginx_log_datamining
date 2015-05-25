#!/usr/bin/env python

from __future__ import print_function
from itertools import groupby
from operator import itemgetter
import sys


def read_mapper_output(file, separator='\t'):
    for line in file:
        yield line.rstrip().split(separator, 1)


def main(separator='\t'):
    # input comes from STDIN (standard input)
    data = read_mapper_output(sys.stdin, separator=separator)
    # groupby groups multiple word-count pairs by word,
    # and creates an iterator that returns consecutive keys and their group:
    # current_word - string containing a word (the key)
    #   group - iterator yielding all ["&lt;current_word&gt;", "&lt;count&gt;"] items
    for cargo, sueldos in groupby(data, itemgetter(0)):
        try:
            sueldos = [int(sueldo) for cargo, sueldo in sueldos]
            total_count = (sum(sueldos) / len(sueldos)) / 100
            print("{}{}{}".format(cargo, separator, total_count))
        except ValueError:
            print("fallo en print", file=sys.stderr)
            pass


if __name__ == "__main__":
    main()
