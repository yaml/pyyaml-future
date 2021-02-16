from .xxx import *
import re, yaml

from yaml.nodes import *

class Library:
    def __init__(self, loader):
        self.loader = loader

        self.add_constructors()

    @classmethod
    def transform_merge(cls, self, node):
        merge = {}
        for subnode in node.value:
            merge.update(
                self.construct_object(subnode, True)
            )
        yield merge

    @classmethod
    def transform_expand(cls, self, node):
        return {'expand': node.value}

    @classmethod
    def transform_import(cls, self, node):
        with open(node.value, 'r') as stream:
            from . import Loader
            loader = Loader(stream)
            return loader.get_single_data()

    @classmethod
    def transform_render(cls, self, node):
        anchors = {}
        for mapping in node.value[1:]:
            pairs = mapping.value
            for pair in pairs:
                anchors[pair[0].value] = pair[1]
        with open(node.value[0].value, 'r') as stream:
            from . import Loader
            loader = Loader(stream)
            loader.anchors = anchors
            return loader.get_single_data()

    def add_constructors(self):
        loader = self.loader
        anchors = loader.anchors

        loader.add_implicit_resolver(
            '!+',
            re.compile('^\+.*\{'),
            None)

        loader.add_implicit_resolver(
            '!+ref',
            re.compile('^\+\*'),
            None)

        loader.add_constructor(
            '!+merge',
            self.__class__.transform_merge)

        loader.add_constructor(
            '!+',
            self.__class__.transform_expand)

        loader.add_constructor(
            '!+import',
            self.__class__.transform_import)

        loader.add_constructor(
            '!+ref',
            self.__class__.transform_ref)

        loader.add_constructor(
            '!+render',
            self.__class__.transform_render)

        loader.add_constructor(
            '!+_deref',
            self.__class__._transform_deref)

        loader.add_constructor(
            '!+_ref-find',
            self.__class__._transform_ref_find)



    @classmethod
    def transform_ref(cls, self, node):
        return self.construct_object(
            self.library.parse_ref(node)
        )

    @classmethod
    def _transform_deref(cls, self, node):
        print(22, self)
        array = node.value
        self.deref_data = None
        for func in array:
            self.deref_data = self.construct_object(func, True)
        return self.deref_data

    @classmethod
    def _transform_ref_find(cls, self, node):
        return self.deref_data.get(node.value)

    def parse_ref(self, node):
        parse = SequenceNode('!+_deref', [])
        ref = node.value[1:]
        while len(ref) > 0:
            alias = re.match('\*(\w+)', ref)
            find = re.match('/(\w+)', ref)
            if alias is not None:
                ref = ref[alias.end():]
                name = alias.group(1)
                parse.value.append(self.loader.anchors[name])
            elif find is not None:
                ref = ref[find.end():]
                key = find.group(1)
                parse.value.append(ScalarNode('!+_ref-find', key))

            else:
                XXX(ref)

        return parse
