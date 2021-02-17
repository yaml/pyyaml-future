import yaml
from yamlfuture import Loader
Loader.anchors = {
    'aaa': {'bbb': 'ccc'},
}
data = yaml.load("yaml stream", Loader=Loader)
