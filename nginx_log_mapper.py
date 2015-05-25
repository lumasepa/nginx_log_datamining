#!/usr/bin/env python

import sys
from hadoop_streaming.base import Mapper
import re


class NginxLogMapper(Mapper):

    @classmethod
    def initialize(cls):
        cls.bot_re = re.compile("[bB]ot")

    @classmethod
    def mapper(cls, data):
        for line in data:
            try:
                ip = line.split()[0]
                uri = line.split('"')[1].split(" ")[1]

                cls.emit(ip, uri)
                cls.emit(uri, 1)

                if cls.bot_re.search(line):
                    cls.emit("BOT", 1)
                else:
                    cls.emit("HUMAN", 1)

            except Exception as e:
                cls.emit("EXCEPTIONS_MAPPER", str(e))


if __name__ == "__main__":
    NginxLogMapper.run()