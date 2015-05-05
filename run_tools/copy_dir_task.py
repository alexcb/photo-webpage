import os.path
import shutil

from run_tools.task import Task


class CopyDirTask(Task):
    def __init__(self, src, dst):
        self._src = src
        self._dst = dst

    def run(self):
        if os.path.exists(self._dst):
            shutil.rmtree(self._dst)
        shutil.copytree(self._src, self._dst)
