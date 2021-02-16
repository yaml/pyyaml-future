import yaml
from yamlfuture import Loader

# This is an example of YAML 1.3:
"""
%yaml 1.3 +yt
---
merged: @merge(*base, *some/foo, @import(other.yaml),
               @render(t1.yaml, xxx: hello))
  foo: 42
  greet: !+ |
    Hello {*some/foo/some}!
"""

# This is a working example in YAML 1.1:

# Terse 1.1 flow version:
stream = """
merged: !+merge [*base, +*some/foo, !+import other.yaml,
                 !+render [ t1.yaml, xxx: hello ], {
  foo: 42,
  greet: !+ "Hello {*some/foo/some}!}\\n"}]
"""

# Fully documented 1.1 block version:
stream = """\
# A merge of 5 mappings into one:
merged: !+merge

  # an alias ref with no anchor defined:
  - *base

  # a ypath query based off an anchor:
  - +*some/foo

  # a yaml file (mapping) import:
  - !+import other.yaml

  # an external template rendering:
  - !+render [ t1.yaml, xxx: hello ]

  # local data mapping:
  - foo: 42               # local data to merge
    # literal scalar string expansion:
    greet: !+ |
      Hello {*some/foo/some}!
"""


Loader.anchors = {
    'base': {'base': 'ball'},
    'some': {'foo': {'some': 'thing'}},
}
data = yaml.load(stream, Loader=Loader)

print(yaml.dump(data, sort_keys=False))
