import pytest

def modules_compile():
    from yamlfuture import Loader
    return "ok"

def test_modules_compile():
    assert modules_compile() == "ok"

def loader_works():
    import yaml
    from yamlfuture import Loader
    yaml.load("", Loader)
    return "ok"

def test_loader_works():
    assert loader_works() == "ok"






def XXX_load_1():
    import yaml
    from yamlfuture import Loader
    Loader.anchors = {
        'aaa': {'bbb': 'ccc'},
    }

    """ Test 1 """
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
