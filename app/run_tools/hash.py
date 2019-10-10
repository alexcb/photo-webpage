import hashlib

class Hasher(object):
    def __init__(self):
        self.hasher = hashlib.md5()

    def add(self, *args):
        for s in args:
            self.hasher.update(s.encode('utf8'))
        return self

    def add_file(self, *paths):
        for path in paths:
            try:
                with open(path, 'rb') as fp:
                    self.hasher.update(b'file exists')
                    self.hasher.update(fp.read())
            except FileNotFoundError:
                self.hasher.update(b'file does not exist')
        return self

    def digest(self):
        return self.hasher.hexdigest()
