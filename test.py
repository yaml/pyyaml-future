import yaml
from yamlfuture import Loader

stream = """\
# A merge of 5 mappings into one:
merged: !+merge           # map merging transform
  - *base                 # an alias ref with no anchor here
#   - +*some/foo            # a ypath query based off an anchor
  - !+import other.yaml   # a yaml file (mapping) import
  - !+render [ t1.yaml,   # an external template rendering
      xxx: hello ]
  - foo: 42               # local data to merge
  - greet: !+ |           # string expansion
      Hello {*name}!

"""

anchors = {
    'base': {'base': 'ball'},
    'some': {'foo': {'some': 'thing'}},
}

loader = Loader()

data = loader.load(stream, anchors=anchors)

print(yaml.dump(data, sort_keys=False))
