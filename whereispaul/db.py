# Copyright (c) Paul Tagliamonte

import gzip
import json

_retry = [2]
_initial = {}

class Database:
    def __init__(self, name, mode='rb'):
        self.name = name
        self.fd = None
        self._load(mode=mode)

    def _load(self, mode='rb'):
        try:
            self.fd = gzip.open(self.name, mode)
            self.data = json.load(self.fd)
        except IOError as e:
            eno = e.errno
            if eno in _retry:
                fd = gzip.open(self.name, 'wb')
                fd.write(json.dumps(_initial))
                fd.close()
                self._load(mode)
            else:
                raise

    def get(self):
        return self.data

    def write(self):
        self.fd.close()
        self.fd = gzip.open(self.name, 'wb')
        self.fd.write(json.dumps(self.data))
        self.fd.close()
        self._load()

    def close(self):
        self.fd.close()
