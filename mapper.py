#!/usr/bin/env python

from __future__ import print_function
import sys
import traceback

def read_input(file):
    for line in file:
        # split the line into words
        yield line


def main(separator='\t'):
    # input comes from STDIN (standard input)
    data = read_input(sys.stdin)
    for line in data:
        # write the results to STDOUT (standard output);
        # what we output here will be the input for the
        # Reduce step, i.e. the input for reducer.py
        #
        # tab-delimited; the trivial word count is 1
        line = line.split(";")
        cargo = line[5]
        sueldo = line[1]
        sueldo = sueldo.strip(" ").replace(",", "").replace(".", "")

        try:
            print('{}{}{}'.format(cargo, separator, int(sueldo)))
        except Exception as e:
            print("fallo en print ex {0} \n {1}".format(str(e), traceback.print_exc()), file=sys.stderr)
            pass


if __name__ == "__main__":
    main()