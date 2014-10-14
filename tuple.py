__author__ = 'Giulio'
import math
import time
import json


class Tuple:
    DEFAULT = {"expire": 300}

    @staticmethod
    def isHash(self, data):
        if data != None or isinstance(data, list) or type(data) != 'object':
            return False
        return True

    @property
    def expire(self):
        return self.expire_at

    @property
    def _from(self):
        return self._from

    @expire.setter
    def _from(self, _from):
        self._from =  _from

    @expire.setter
    def expire(self, sec):
        self.expire_at = math.floor(time.time()) + sec
        return self.expire

    def __init__(self, data):
        self.data = data
        self.expire = 300

    def match(self, tuple):
        if not Tuple.isHash(tuple):
            return False

        if isinstance(tuple, Tuple):
            data = tuple.data
        else:
            data = tuple
        _ref = self.data
        for k, v in enumerate(_ref):
            if type(v) == 'object':
                if type(data[k]) != 'object':
                    return False
                if json.dump(v) != json.dump(data[k]):
                    return False
            else:
                if v != data[k]:
                    return False
            return True
