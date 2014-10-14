__author__ = 'Giulio'

import time
from tuple import Tuple
from multiprocessing.dummy import Pool
from functools import partial
pool = Pool(processes=1)

class TupleSpace:

    def async_function(self):
        """
        Function we want to run asynchronously and in parallel,
        usually one with heavy input/output, though using a
        dummy function here.
        """
        time.sleep(1)
        return None

    @property
    def size(self):
        return len(self.tuples)

    def __init__(self, name):
        if name != None:
            self.name = name
        else:
            self.name = 'nonome'
        self.tuples = []
        self.callback = []

    def write(self, tuple, options = None ):
        i = _i = 0
        called = []
        taked = False
        _ref = len(self.callback)

        # c, called, taked, _j, _ref = None
        if options == None:
            options = {
                'expire' : Tuple.DEFAULT.get('expire')
            }
        if not Tuple.isHash(tuple) and not isinstance(tuple, Tuple):
            return
        if not isinstance(tuple, Tuple):
            tuple = Tuple(tuple)
        exp = options.get('expire')
        if type(exp) == 'number' and exp > 0:
            tuple.expire = exp
        else:
            tuple.expire = Tuple.DEFAULT.get('expire')
        tuple._from = options.get('from')

        while ((0 <= _ref and _i < _ref) or (0 > _ref and _i > _ref)):
            c = self.callback[i]
            ctuple = c.get('tuple')
            ctype = c.get('type')
            if ctuple.match(tuple):
                if ctype == 'take' or ctype == 'read':
                    called.append(i)

                callback_func = partial(c.callback, None, tuple)
                pool = Pool(processes=1)
                pool.apply_async(
                    self.async_function,
                    args=[c],
                    callback=callback_func
                )
                if ctype == 'take':
                    taked = True
                    break;

            if (0 <= _ref):
                _i = _i + 1
            else:
                _i = _i - 1
            i = _i