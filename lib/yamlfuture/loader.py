from .xxx import *
__all__ = ['Loader']

from yaml import SafeLoader, composer, representer

from .stdlib import Library

class Loader(SafeLoader):

    def __init__( self, stream=''):
        SafeLoader.__init__(self, stream)
        self.represent = representer.Representer().represent_data

    def load(self, stream=None, anchors=None):
        if stream is not None:
            SafeLoader.__init__(self, stream)

        if anchors is not None:
            self.set_anchors(anchors)

        self.library = Library(self)

        data = self.get_single_data()
        return data

    def set_anchors(self, anchors):
        self.anchors = {}

        for key in anchors:
            self.anchors[key] = self.represent(anchors[key])

    def compose_document(self):
        anchors = self.anchors
        node = composer.Composer.compose_document(self)
        self.anchors = anchors
        return node
