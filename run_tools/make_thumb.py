from run_tools.task import Task

import Image


thumbnail_width = 300
thumbnail_height = 300


class MakeThumb(Task):
    def __init__(self, image_path, thumbnail_path):
        self._input_path = image_path
        self._output_path = thumbnail_path

    def run(self):
        im = Image.open(self._input_path)
        current_width, current_height = im.size

        resize_ratio_width = (current_width / float(thumbnail_width))
        resize_ratio_height = (current_height / float(thumbnail_height))

        resize_ratio = max(resize_ratio_width, resize_ratio_height)
            
        resize_width = int(current_width / resize_ratio)
        resize_height = int(current_height / resize_ratio)

        im.thumbnail((resize_width, resize_height), Image.ANTIALIAS)
        im.save(self._output_path, "JPEG")
