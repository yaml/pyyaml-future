pyyaml-future
=============

Use YAML 1.3 Features in PyYAML (YAML 1.1)

## Synopsis
```
import yaml
from yamlfuture import Loader

Loader.anchors = {'name': 'YAML'}

text = """\
greeting: !+ |
  Hello {*name}.
  Welcome to the future!
"""

print(yaml.dump(yaml.load(text, Loader))
```

## Description

YAML 1.3 is bringing excited new features to YAML (while keeping the YAML you
know and love (or hate) the same).

This package lets you use the new features (or close approximations) in PyYAML
now.

This is the first release.
More features and documentation coming soon.

## License & Copyright

This project is licensed under the terms of the `MIT` license.
See [LICENSE](https://github.com/yaml/pyyaml-future/blob/main/LICENSE) for more details.

Copyright 2021 Ingy döt Net <ingy@ingy.net>
