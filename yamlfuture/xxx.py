def YYY(o):
    import yaml
    print(yaml.dump(o, explicit_start=True, explicit_end=True, sort_keys=False))
    return o

def XXX(o):
    import yaml
    print(yaml.dump(o, explicit_start=True, explicit_end=True, sort_keys=False))
    import sys
    sys.exit(1)
