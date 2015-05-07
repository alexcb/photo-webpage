import hashlib
import shutil
import os

import Image

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
                'input_path': image_path,
                'thumbnail_name': thumbnail,
                'output_name': output_name
                })

    def get_dependencies(self):
        yield LambdaTask(lambda: mkdir_parents(self._gallery_build_path))
        for photo in self._photos:
            yield LambdaTask(lambda: shutil.copyfile(
                src=photo['input_path'],
                dst=os.path.join(self._gallery_build_path, photo['output_name']),
                ))
            yield MakeThumb(
                photo['input_path'],
                os.path.join(self._gallery_build_path, photo['thumbnail_name'])
                )

    def run(self):
        template = self._template_env.get_template( 'gallery.jinja' )

        thumbnails = []
        total_photos = len(self._photos)
        for i, photo in enumerate(self._photos):
            im = Image.open(os.path.join(self._gallery_build_path, photo['thumbnail_name']))
            image_width, image_height = im.size

            thumbnails.append({
                'url': photo['output_name'],
                'thumbnail': photo['thumbnail_name'],
                'width': image_width,
                'height': image_height,
                'title': 'TODO (%s of %s)' % (i+1, total_photos)
                })

        with open(os.path.join(self._gallery_build_path, 'index.html'), 'w') as fp:
            fp.write(template.render({
                'photos': thumbnails,
                }))
