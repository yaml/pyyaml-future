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
            self.add_transform_ref(loader))

        loader.add_constructor(
            '!+render',
            self.__class__.transform_render)

        loader.add_constructor(
            '!+_deref',
            self.__class__.transform_deref)



    def add_transform_ref(self, loader):
        #print(11, loader, loader.anchors)
        def transform_ref(this, node):
            return this.construct_object(
                self.parse_ref(node)
            )
        return transform_ref

    @classmethod
    def transform_deref(cls, self, node):
        print(22, node)
        array = node.value
        self.deref_data = None
        for func in array[1:]:
            self.deref_data = self.construct_object(func, True)
        XXX(self.deref_data)

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
                parse.value.append(ScalarNode('!++ref-find', key))

            else:
                XXX(ref)

        return parse
        return MappingNode(
            tag='tag:yaml.org,2002:map',
            value=[(
                ScalarNode(tag='tag:yaml.org,2002:str', value='qwerty'),
                ScalarNode(tag='tag:yaml.org,2002:str', value='qwerty'))])
        # SequenceNode(
        #   tag='!+_dereference',
        #   value=[
        #     ScalarNode(tag='tag:yaml.org,2002:int', value='123'),
        #     ScalarNode(tag='!ref-find', value='foo'

