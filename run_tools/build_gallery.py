import hashlib
import shutil
import os

from run_tools.task import Task
from run_tools.utils import LambdaTask, mkdir_parents
from run_tools.make_thumb import MakeThumb


def get_image_output_name(image_path):
    hexdigest = hashlib.md5(open(image_path, 'rb').read()).hexdigest()
    return 'alexcb_photo_mofo_ca_%s' % hexdigest


class BuildGallery(Task):
    def __init__(self, gallery_path, gallery_build_path, template_env):
        self._gallery_build_path = gallery_build_path
        self._gallery_path = gallery_path
        self._template_env = template_env
        self._photos = []
        for x in os.listdir(gallery_path):
            image_path = os.path.join(gallery_path, x)
            output_name = get_image_output_name(image_path)
            thumbnail = 'thumbnail_%s' % output_name
            self._photos.append({
                'thumbnail': thumbnail,
                'input_path': image_path,
                'url': output_name,
                'output_path': os.path.join(gallery_build_path, output_name),
                'thumbnail_path': os.path.join(gallery_build_path, thumbnail),
                })

    def get_dependencies(self):
        yield LambdaTask(lambda: mkdir_parents(self._gallery_build_path))
        for photo in self._photos:
            yield LambdaTask(lambda: shutil.copyfile(photo['input_path'], photo['output_path']))
            yield MakeThumb(photo['input_path'], photo['thumbnail_path'])

    def run(self):
        template = self._template_env.get_template( 'gallery.jinja' )

        with open(os.path.join(self._gallery_build_path, 'index.html'), 'w') as fp:
            fp.write(template.render({
                'photos': self._photos,
                }))
