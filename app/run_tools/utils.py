import os
import errno

from run_tools.task import Task

def mkdir_parents(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


class LambdaTask(Task):
    def __init__(self, method, name):
        self._method = method
        self._name = name

    def name(self):
        return self._name

    def run(self):
        self._method()


class MkdirTask(Task):
    def __init__(self, path):
        self._path = path

    def name(self):
        return 'mkdir ' + self._path

    def run(self):
        mkdir_parents(self._path)
