pyyaml-future
=============

Use YAML 1.3 Features in PyYAML (YAML 1.1)

## Synopsis
```
import yaml
from yamlfuture import Loader

Loader.anchors = {'name': 'YAML'}

stream = """\
---
greeting: !+ |
  Hello {*name}.
  Welcome to the future!
copyright: !+import [../data.yaml, /copyright/year]

"""

print(yaml.dump(yaml.load(stream, Loader))
```

## Status

This module is *very* **ALPHA**.

YAML 1.3 is still being defined.
As the various features of the YAML 1.3 evolve, `yamlfuture` will evolve.

Use with caution for now.

## Description

YAML 1.3 is bringing exciting new features to YAML (while keeping the YAML you
know and love (or hate) the same).

This package lets you use the new features (or close approximations) in PyYAML
now.

This is a very early release.
More features and documentation coming soon.

## Features

* Merge a sequence of mappings:
  ```
  merged: !+merge [*map1, *map2, foo: bar]
  ```

* Define anchors (from Python) outside the YAML stream:
  ```
  Loader.anchors = {"name": "world"}
  yaml.load("hello: *name", Loader)
  ```

* Use aliases with paths:
  ```
  value: &foo
    yaml: future
  when: +*foo/yaml
  absolute: /foo/0/bar
  siblings:
    a: 2
    b: 4
    all: [+*:a, +*:b]
  foo: { bar: +*../../siblings/a }
  ```

* String interpolation:
  ```
  greeting: !+ Hello {*name}!
  ```

* Import other YAML files into any node:
  ```
  foo: !+import foo.yaml
  bar: !+import [foo.yaml, /0/bar]
  ```

* Import/render external "template" yaml files:
  ```
  # file 'template.yaml'
  foo:
    bar: *value

  # file 'main.yaml'
  foo bar: !+render [template.yaml, value: baz]
  ```

## License & Copyright

This project is licensed under the terms of the `MIT` license.
See [LICENSE](https://github.com/yaml/pyyaml-future/blob/main/LICENSE) for more details.

Copyright 2021 Ingy döt Net <ingy@ingy.net>
