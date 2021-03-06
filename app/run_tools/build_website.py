import os
import shutil

from run_tools.task import Task
from run_tools.utils import MkdirTask
from run_tools.build_blog import BuildBlog
from run_tools.build_gallery import BuildGallery
from run_tools.build_page import BuildPage
from run_tools.copy_dir_task import CopyDirTask
from run_tools.copy_task import CopyTask


class BuildWebsite(Task):
    def __init__(self, config, static_path, photos_path, blog_dir, build_dir, template_env):
        self._config = config
        self._static_path = static_path
        self._template_env = template_env
        self._build_dir = build_dir
        self._blog_dir = blog_dir
        self._blog_output_dir = os.path.join(build_dir, 'blog')

        try:
            index_gallery = self._config['galleries']['index']
        except:
            index_gallery = config['galleries']['order'][0]

        self._photo_galleries = []
        for gallery_name in config['galleries']['order']:
            if index_gallery == gallery_name:
                html_file_name = 'index.html'
            else:
                html_file_name = '%s.html' % gallery_name.lower().replace(' ', '')

            self._photo_galleries.append({
                'name': gallery_name,
                'url': html_file_name,
                'input_photos_dir': os.path.join(photos_path, gallery_name),
                'output_photos_dir': os.path.join(build_dir, 'photos'),
                'output_html_path': os.path.join(build_dir, html_file_name)
                })

    def name(self):
        return 'BuildWebsite'

    def get_dependencies(self):
        yield MkdirTask(self._build_dir)
        yield CopyDirTask(self._static_path, os.path.join(self._build_dir, 'static'))
        yield CopyTask(os.path.join(self._static_path, 'favicon.ico'), os.path.join(self._build_dir, 'favicon.ico'))

        gallery_order = self._config['galleries']['order']
        gallery_links = [{
            'name': x['name'],
            'url': x['url'],
            } for x in self._photo_galleries]

        for gallery in self._photo_galleries:
            yield BuildGallery(
                gallery_links = gallery_links,
                config = self._config,
                input_photos_dir = gallery['input_photos_dir'],
                output_html_path = gallery['output_html_path'],
                output_photos_dir = gallery['output_photos_dir'],
                template_env = self._template_env,
                )

        for template, output_filename in (
                #('about.jinja', 'about.html'),
                ('contact.jinja', 'contact.html'),
                ):
            yield BuildPage(
                template = template,
                output_path = os.path.join(self._build_dir, output_filename),
                gallery_links = gallery_links,
                template_env = self._template_env,
                )

        yield BuildBlog(self._config, gallery_links, self._blog_dir, self._template_env, self._blog_output_dir)

    def run(self):
        pass
