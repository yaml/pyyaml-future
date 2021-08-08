import yaml
from yamlfuture import Loader

stream = """\
# A merge of 5 mappings into one:
merged: !merge

# an alias ref with no anchor defined:
- *base

# a ypath query based off an anchor:
- +*some/foo

# a yaml file (mapping) import:
- !import other.yaml

# an external template rendering:
- !render [ t1.yaml, xxx: hello ]

# local data mapping:
- foo: 42               # local data to merge

# literal scalar string expansion:
greet: !+ |
    Hello {*some/foo/some}!
"""

Loader.filepath = __file__

Loader.anchors = {
    'base': {'base': 'ball'},
    'some': {'foo': {'some': 'thing'}},
}
data = yaml.load(stream, Loader)

print(yaml.dump(data))
