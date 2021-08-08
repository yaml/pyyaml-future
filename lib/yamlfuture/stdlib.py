from .xxx import *
import os, re

from yaml.nodes import *

class Library:
    def __init__(self, loader):
        self.loader = loader
        self.add_constructors()

    @classmethod
    def _read_import_file(cls, self, path):
        if self.importpath is None:
            raise Exception("Loader.filepath not set")
        importpath = os.path.join(self.importpath, path)
        with open(importpath, 'r') as stream:
            text = stream.read()
        return text

    @classmethod
    def transform_expand(cls, self, node):
        return self.construct_object(
            self.library.parse_expansion(node)
        )

    @classmethod
    def transform_import(cls, self, node):
        stream = cls._read_import_file(self, node.value)
        from . import Loader
        loader = Loader(stream)
        return loader.get_single_data()

    @classmethod
    def transform_join(cls, self, node):
        join = []
        for subnode in node.value:
            join.append(
                self.construct_object(subnode, True)
            )
        yield ''.join(join)

    @classmethod
    def transform_merge(cls, self, node):
        merge = {}
        for subnode in node.value:
            merge.update(
                self.construct_object(subnode, True)
            )
        yield merge

    @classmethod
    def transform_render(cls, self, node):
        anchors = {}
        for mapping in node.value[1:]:
            pairs = mapping.value
            for pair in pairs:
                anchors[pair[0].value] = pair[1]
        stream = cls._read_import_file(self, node.value[0].value)
        from . import Loader
        loader = Loader(stream)
        loader.anchors = anchors
        return loader.get_single_data()

    @classmethod
    def transform_ref(cls, self, node):
        return self.construct_object(
            self.library.parse_reference(node)
        )

    # Internal expansion tags:
    @classmethod
    def _transform_deref(cls, self, node):
        array = node.value
        self.deref_data = None
        for func in array:
            self.deref_data = self.construct_object(func, True)
        return self.deref_data

    @classmethod
    def _transform_ref_find(cls, self, node):
        return self.deref_data.get(node.value)

    @classmethod
    def _transform_ref_sibling(cls, self, node):
        return node.value.upper()


    # Add up the resolver and constructor settings:
    def add_constructors(self):
        loader = self.loader
        anchors = loader.anchors

        loader.add_implicit_resolver(
            '!+',
            re.compile(r'^\+.*\{'),
            None)

        loader.add_implicit_resolver(
            '!ref',
            re.compile(r'^\+\*'),
            None)

        loader.add_constructor(
            '!+',
            self.__class__.transform_expand)

        loader.add_constructor(
            '!merge',
            self.__class__.transform_merge)

        loader.add_constructor(
            '!import',
            self.__class__.transform_import)

        loader.add_constructor(
            '!join',
            self.__class__.transform_join)

        loader.add_constructor(
            '!ref',
            self.__class__.transform_ref)

        loader.add_constructor(
            '!render',
            self.__class__.transform_render)

        # Internal tag constructors:
        loader.add_constructor(
            '!_deref',
            self.__class__._transform_deref)

        loader.add_constructor(
            '!_ref-find',
            self.__class__._transform_ref_find)

        loader.add_constructor(
            '!_ref-sibling',
            self.__class__._transform_ref_sibling)


    # TODO move parsers to another class?
    def parse_reference(self, node, bare=False):
        parse = SequenceNode('!_deref', [])
        if bare:
            ref = node
        else:
            ref = node.value[1:]
        while len(ref) > 0:
            alias = re.match(r'\*(\w+)', ref)
            sibling = re.match(r'\*:(\w+)', ref)
            find = re.match(r'/(\w+)', ref)
            if alias is not None:
                ref = ref[alias.end():]
                name = alias.group(1)
                parse.value.append(self.loader.anchors[name])
            elif sibling is not None:
                ref = ref[sibling.end():]
                key = sibling.group(1)
                parse.value.append(ScalarNode('!_ref-sibling', key))
            elif find is not None:
                ref = ref[find.end():]
                key = find.group(1)
                parse.value.append(ScalarNode('!_ref-find', key))

            else:
                XXX(ref)

        return parse

    def parse_expansion(self, node):
        parse = SequenceNode('!join', [])
        scalar = node.value[0:]
        scalar = re.sub(r'^\+`', '', scalar)
        scalar = re.sub(r'^`', '', scalar)
        scalar = re.sub(r'`$', '', scalar)
        while len(scalar) > 0:
            string = re.match(r'([^\{]+)', scalar)
            expand = re.match(r'\{(.*?)\}', scalar)
            if string is not None:
                scalar = scalar[string.end():]
                text = string.group(1)
                parse.value.append(
                    ScalarNode('tag:yaml.org,2002:str', text))
            elif expand is not None:
                scalar = scalar[expand.end():]
                query = expand.group(1)
                parse.value.append(self.parse_reference(query, True))

            else:
                XXX(scalar)

        return parse
