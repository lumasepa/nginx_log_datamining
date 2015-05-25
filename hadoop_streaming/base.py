from __future__ import print_function
from itertools import groupby
from operator import itemgetter
import sys


class Mapper(object):
    separator = "\t"

    @classmethod
    def initialize(cls):
        pass

    @classmethod
    def emit(cls, key, value):
        print('{}{}{}'.format(key, cls.separator, value))

    @classmethod
    def _read_input(cls, stdin):
        for line in stdin:
            yield line

    @classmethod
    def mapper(cls, data):
        raise NotImplementedError("You must implement this method")

    @classmethod
    def run(cls):
        cls.initialize()
        cls.mapper(cls._read_input(sys.stdin))


class Reducer(object):
    separator = "\t"

    @classmethod
    def initialize(cls):
        pass

    @classmethod
    def emit(cls, key, value):
        print('{}{}{}'.format(key, cls.separator, value))

    @classmethod
    def run(cls):
        cls.initialize()

        def itermap():
            for key, values in groupby(cls._read_mapper_output(sys.stdin), itemgetter(0)):
                yield key, [value for key, value in values]

        for key, values in itermap():
            cls.reducer(key, values)

    @classmethod
    def _read_mapper_output(cls, stdin):
        for line in stdin:
            yield line.rstrip().split(cls.separator, 1)

    @classmethod
    def reducer(cls, key, values):
        raise NotImplementedError("you must implement this method")