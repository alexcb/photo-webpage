from run_tools.task import Task


class BuildPage(Task):
    def __init__(self, gallery_links, template, output_path, template_env):
        self._gallery_links = gallery_links
        self._template = template
        self._template_env = template_env
        self._output_path = output_path

    def name(self):
        return 'BuildPage ' + self._template

    def run(self):
        template = self._template_env.get_template( self._template )
        with open(self._output_path, 'w') as fp:
            fp.write(template.render({
                'galleries': self._gallery_links,
                }))
