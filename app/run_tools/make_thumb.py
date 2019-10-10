from run_tools.task import Task
from run_tools.hash import Hasher

from PIL import Image


class MakeThumb(Task):
    def __init__(self, image_path, thumbnail_path, max_width, max_height):
        self._max_width = max_width
        self._max_height = max_height
        self._input_path = image_path
        self._output_path = thumbnail_path

    def input_digest(self):
        return Hasher().add(
                self.__class__.__name__,
                str(self._max_width),
                str(self._max_height),
            ).add_file(
                self._input_path,
            ).digest()

    def output_digest(self):
        return Hasher().add_file(self._output_path).digest()

    def name(self):
        return self.__class__.__name__ + ' ' + self._input_path + ' -> ' + self._output_path

    def run(self):
        im = Image.open(self._input_path)
        current_width, current_height = im.size

        resize_ratio_width = (current_width / float(self._max_width))
        resize_ratio_height = (current_height / float(self._max_height))

        if resize_ratio_height < 1.0 or resize_ratio_width < 1.0:
            raise RuntimeError('Image %s smaller (%s x %s) than thumbnail size (%s x %s)' %
                (self._input_path, current_width, current_height, self._max_width, self._max_height))

        resize_ratio = max(resize_ratio_width, resize_ratio_height)
  
        resize_width = int(current_width / resize_ratio)
        resize_height = int(current_height / resize_ratio)

        im.thumbnail((resize_width, resize_height), Image.ANTIALIAS)
        im.save(self._output_path, "JPEG")
