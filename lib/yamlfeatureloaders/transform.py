import re, yaml
from yaml.nodes import *
from yaml.composer import *
from yaml.constructor import *
from yaml.loader import *

class TransformConstructor(SafeConstructor):
    def transform_import(self, node):
        with open(node.value, 'r') as stream:
            loader = TransformLoader(stream)
            return loader.get_single_data()

    def transform_merge(self, node):
        merge = {}
        yield merge
        for subnode in node.value:
            merge.update(
                self.construct_object(subnode, True)
            )

    def transform_ref(self, node):
        return {'XXX-!@ref': node.value}

    def transform_render(self, node):
        anchors = {}
        for mapping in node.value[1:]:
            pairs = mapping.value
            for pair in pairs:
                anchors[pair[0].value] = pair[1]
        with open(node.value[0].value, 'r') as stream:
            loader = TransformLoader(stream)
            loader.anchors = anchors
            return loader.get_single_data()

TransformConstructor.add_constructor(
    '!@import',
    TransformConstructor.transform_import,
)

TransformConstructor.add_constructor(
    '!@merge',
    TransformConstructor.transform_merge,
)

TransformConstructor.add_constructor(
    '!@ref',
    TransformConstructor.transform_ref,
)

TransformConstructor.add_constructor(
    '!@render',
    TransformConstructor.transform_render,
)

class TransformLoader(TransformConstructor, SafeLoader):

    def __init__(self, stream=None):
        if stream is not None:
            SafeLoader.__init__(self, stream)

    def set_anchors(self, anchors):
        self.anchors = {}
        for key in anchors:
            self.anchors[key] = yaml.compose(yaml.dump(anchors[key]))

    def load(self, stream):
        anchors = self.anchors
        SafeLoader.__init__(self, stream)
        self.anchors = anchors
        return self.get_single_data()


TransformLoader.add_implicit_resolver(
    '!@ref',
    re.compile('^=\*'),
    None,
)
