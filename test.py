import yaml
from yamlfeatureloaders import *

yaml_stream = """\
# A merge of 5 mappings into one:
--- !@merge             # map merging transform
- *base                 # an alias ref with no anchor here
- =*some/foo            # a ypath query based off an anchor
- !@import other.yaml   # a yaml file (mapping) import
- !@render [ t1.yaml,   # an external template rendering
    xxx: hello ]
- foo: 42               # local data to merge
"""

loader = TransformLoader()
loader.set_anchors({
    'base': {'base': 'ball'},
})
data = loader.load(yaml_stream)

print(yaml.dump(data))
