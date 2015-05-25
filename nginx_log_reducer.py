#!/usr/bin/env python
import sys
from hadoop_streaming.base import Reducer
import re

class NginxLogReducer(Reducer):
    @classmethod
    def initialize(cls):
        cls.ip_re = re.compile(r"[0-9]+(?:\.[0-9]+){3}")

    @classmethod
    def reducer(cls, key, values):
            try:
                if key == "BOT":
                    cls.emit("BOT", sum(map(lambda x: int(x), values)))

                elif key == "HUMAN":
                    cls.emit("HUMAN", sum(map(lambda x: int(x), values)))

                elif cls.ip_re.match(key) or key == "EXCEPTIONS_MAPPER":
                    cls.emit(key, values)

                else:
                    cls.emit(key, sum(map(lambda x: int(x), values)))

            except Exception as e:
                cls.emit("EXCEPTIONS_REDUCER", str(e))

if __name__ == "__main__":
    NginxLogReducer.run()
