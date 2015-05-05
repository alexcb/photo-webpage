import os
import shutil

from run_tools.task import Task
from run_tools.utils import LambdaTask, mkdir_parents
from run_tools.build_gallery import BuildGallery
from run_tools.copy_dir_task import CopyDirTask


class BuildWebsite(Task):
    def __init__(self, static_path, photos_path, build_dir, template_env):
        self._static_path = static_path
        self._template_env = template_env
        self._photo_galleries = [
            {
                'gallery': x,
                'path': os.path.join(photos_path, x),
                'build_path': os.path.join(build_dir, x),
                }
            for x in os.listdir(photos_path)
            ]
        self._build_dir = build_dir

    def get_dependencies(self):
        yield LambdaTask(lambda: mkdir_parents(self._build_dir))
        yield CopyDirTask(self._static_path, os.path.join(self._build_dir, 'static'))
        for gallery in self._photo_galleries:
            yield BuildGallery(
                gallery_path = gallery['path'],
                gallery_build_path = gallery['build_path'],
                template_env = self._template_env,
                )

    def run(self):
        template = self._template_env.get_template( 'index.jinja' )

        with open(os.path.join(self._build_dir, 'index.html'), 'w') as fp:
            fp.write(template.render({
                'galleries': self._photo_galleries,
                }))
