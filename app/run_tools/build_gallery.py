import hashlib
import shutil
import os
import yaml

from PIL import Image

from run_tools.task import Task
from run_tools.utils import MkdirTask
from run_tools.make_thumb import MakeThumb
from run_tools.make_image import MakeImage


def get_image_output_name(image_prefix, image_path):
    hexdigest = hashlib.md5(open(image_path, 'rb').read()).hexdigest()
    return '%s%s.jpg' % (image_prefix, hexdigest)

def get_meta(path):
    if not os.path.exists(path):
        return {}
    with open(path) as fp:
        print(path)
        return yaml.load(fp)


class BuildGallery(Task):
    def __init__(self, gallery_links, config, input_photos_dir, output_html_path, output_photos_dir, template_env):
        self._gallery_links = gallery_links
        self._config = config
        self._input_photos_dir = input_photos_dir
        self._output_html_path = output_html_path
        self._output_photos_dir = output_photos_dir
        self._template_env = template_env

        self._thumbnails_to_make = []
        self._images_to_make = []
        self._photos = []

        meta = get_meta(os.path.join(self._input_photos_dir, 'meta.yaml'))


        for x in reversed(sorted(x for x in os.listdir(self._input_photos_dir) if x.endswith('jpg'))):
            image_path = os.path.join(self._input_photos_dir, x)
            output_name = get_image_output_name(self._config['image_prefix'], image_path)
            thumbnail = 'thumbnail_%s' % output_name
            self._thumbnails_to_make.append({
                'input_path': image_path,
                'output_path': os.path.join(self._output_photos_dir, thumbnail),
                })

            self._images_to_make.append({
                'input_path': image_path,
                'output_path': os.path.join(self._output_photos_dir, output_name),
                })

            self._photos.append({
                'input_path': image_path,
                'thumbnail': thumbnail,
                'fullsize': output_name,
                'title': meta.get(x, 'untitled'),
                })

    def name(self):
        return 'BuildGallery ' + self._input_photos_dir

    def get_dependencies(self):
        yield MkdirTask(self._output_photos_dir)
        for thumbnail in self._thumbnails_to_make:
            yield MakeThumb(
                thumbnail['input_path'],
                thumbnail['output_path'],
                max_width = self._config['thumbnails']['max_width'],
                max_height = self._config['thumbnails']['max_height'],
                )
        for img in self._images_to_make:
            yield MakeImage(
                img['input_path'],
                img['output_path'],
                max_width = self._config['images']['max_width'],
                max_height = self._config['images']['max_height'],
                )

        #for photo in self._photos:
        #    yield LambdaTask(lambda: shutil.copyfile(
        #        src=photo['input_path'],
        #        dst=os.path.join(self._output_photos_dir, photo['fullsize']),
        #        ))

    def _get_image_dimension(self, image_name):
        im = Image.open(os.path.join(self._output_photos_dir, image_name))
        image_width, image_height = im.size
        return image_width, image_height

    def run(self):
        template = self._template_env.get_template( 'gallery.jinja' )

        thumbnails = []
        total_photos = len(self._photos)
        for i, photo in enumerate(self._photos):
            image_width, image_height = self._get_image_dimension(photo['thumbnail'])

            thumbnails.append({
                'url': photo['fullsize'],
                'thumbnail': photo['thumbnail'],
                'width': image_width,
                'height': image_height,
                'title': photo['title'],
                })

        with open(self._output_html_path, 'w') as fp:
            fp.write(template.render({
                'photos': thumbnails,
                'galleries': self._gallery_links,
                }))
