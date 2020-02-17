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
from run_tools.build_blog_entry import BuildBlogEntry

def get_image_output_name(image_prefix, image_path):
    hexdigest = hashlib.md5(open(image_path, 'rb').read()).hexdigest()
    return '%s%s.jpg' % (image_prefix, hexdigest)

def must_trim_prefix(s, prefix):
    assert s.startswith(prefix)
    return s[len(prefix):]

class BuildBlog(Task):
    def __init__(self, config, gallery_links, blog_input, template_env, blog_output_dir):
        self._blog_input = blog_input
        self._blog_output_dir = blog_output_dir
        self._blog_output_html = os.path.join(blog_output_dir, 'index.html')
        self._template_env = template_env
        self._gallery_links = gallery_links
        self._config = config

        if not self._blog_input.endswith('/'):
            self._blog_input += '/'

        self._images_to_make = []
        self._image_map = {}
        for dirname, subdirs, files in os.walk(self._blog_input):
            dirname = must_trim_prefix(dirname, self._blog_input)
            for f in files:
                if f.endswith('.jpg'):
                    image_path = os.path.join(dirname, f)
                    abs_image_path = os.path.join(self._blog_input, image_path)
                    output_name = get_image_output_name(self._config['image_prefix'], abs_image_path)
                    self._images_to_make.append({
                        'input_path': abs_image_path,
                        'output_path': os.path.join(self._blog_output_dir, output_name),
                        })
                    self._image_map[image_path] = output_name

        self._blog_entries_to_make = []
        for x in reversed(sorted(x for x in os.listdir(self._blog_input))):
            path = os.path.join(self._blog_input, x)
            if os.path.isdir(path):
                self._blog_entries_to_make.append(x)

    def name(self):
        return 'BuildBlog'

    def get_dependencies(self):
        yield MkdirTask(self._blog_output_dir)

        for img in self._images_to_make:
            yield MakeImage(
                img['input_path'],
                img['output_path'],
                max_width = self._config['blog']['max_width'],
                max_height = self._config['blog']['max_height'],
                )

            for x in self._blog_entries_to_make:
                yield BuildBlogEntry(self._template_env, self._config, self._gallery_links, self._blog_input, x, self._blog_output_dir, self._image_map)

    def get_date(self, s):
        m = re.search("([0-9]{4}\-[0-9]{2}\-[0-9]{2})-", s)
        return m.group(1)


    def run(self):
        blog_posts = []
        for x in self._blog_entries_to_make:
            info_path = os.path.join(self._blog_input, x, 'info.yml')
            rel_img = os.path.join(x, 'title.jpg')
            print(rel_img)
            print(self._image_map)
            title_img = self._image_map[rel_img]

            date = self.get_date(x)

            with open(info_path) as fp:
                info = yaml.load(fp)

            blog_posts.append({
                'url': f'/blog/{x}.html',
                'img': title_img,
                'title': info['title'],
                'date': date,
                })

        template = self._template_env.get_template( 'blog.jinja' )
        with open(self._blog_output_html, 'w') as fp:
            fp.write(template.render({
                'galleries': self._gallery_links,
                'blog_posts': blog_posts,
                }))

