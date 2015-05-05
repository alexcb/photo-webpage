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
    def __init__(self, method):
        self._method = method

    def run(self):
        self._method()
