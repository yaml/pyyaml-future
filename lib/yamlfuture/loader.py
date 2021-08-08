import os
from .xxx import *
__all__ = ['Loader']

from yaml import SafeLoader, composer, representer

from .stdlib import Library

class Loader(SafeLoader):
    anchors = None
    filepath = None

    def __init__(self, stream):
        SafeLoader.__init__(self, stream)
        self.library = Library(self)
        self.represent = representer.Representer().represent_data
        if Loader.anchors is not None:
            self.set_anchors(Loader.anchors)
        if Loader.filepath is None:
            self.importpath = os.getcwd()
        else:
            self.importpath = os.path.abspath(
                os.path.dirname(Loader.filepath))

    def set_anchors(self, anchors):
        self.anchors = {}

        for key in anchors:
            self.anchors[key] = self.represent(anchors[key])

    def compose_document(self):
        anchors = self.anchors
        node = composer.Composer.compose_document(self)
        self.anchors = anchors
        return node
