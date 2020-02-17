import hashlib
import shutil
import os
import yaml
import re

from PIL import Image

from run_tools.task import Task
from run_tools.utils import MkdirTask
from run_tools.make_thumb import MakeThumb
from run_tools.make_image import MakeImage

class BuildBlogEntry(Task):
    def __init__(self, template_env, config, gallery_links, blog_input_path, blog_entry_name, output_dir, image_mapping):
        self._template_env = template_env
        self._config = config
        self._gallery_links = gallery_links
        self.blog_input_path = blog_input_path
        self.blog_entry_name = blog_entry_name
        self.output_dir = output_dir
        self.image_mapping = image_mapping

        self._blog_output_html = os.path.join(output_dir, blog_entry_name + '.html')

    def name(self):
        return 'BuildBlogEntry'

    def get_dependencies(self):
        yield from []

    def create_html(self, text):
        html = []
        images = re.findall(r'[a-zA-Z0-9_]+\.jpg', text)
        for img in images:
            hashed_url = self.image_mapping[os.path.join(self.blog_entry_name, img)]
            text = text.replace(img, f'<img src="{hashed_url}" />')

        for l in text.split('\n'):
            html.append(f'<p>{l}</p>')
        return ''.join(html)

    def get_date(self, s):
        m = re.search("([0-9]{4}\-[0-9]{2}\-[0-9]{2})-", s)
        return m.group(1)

    def run(self):
        info_path = os.path.join(self.blog_input_path, self.blog_entry_name, 'info.yml')
        with open(info_path) as fp:
            info = yaml.load(fp)

        template = self._template_env.get_template( 'blog_entry.jinja' )
        with open(self._blog_output_html, 'w') as fp:
            fp.write(template.render({
                'galleries': self._gallery_links,
                'title': info['title'],
                'date': self.get_date(self.blog_entry_name),
                'text': self.create_html(info['text']),
                }))


