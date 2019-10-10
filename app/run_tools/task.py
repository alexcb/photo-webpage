class Task(object):
    def __init__(self):
        pass

    def get_dependencies(self):
        return iter([])

    def input_digest(self):
        return None

    def output_digest(self):
        return None

    def name(self):
        return 'unknown task'

    def run(self):
        pass
