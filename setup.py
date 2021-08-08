version = '0.0.5'

from setuptools import setup
import pathlib

root = pathlib.Path(__file__).parent.resolve()

long_description = \
  (root / '.long_description.md') \
  .read_text(encoding='utf-8')

setup(
  name = 'pyyaml-future',
  version = version,
  description = 'Use YAML 1.3 Features in PyYAML (YAML 1.1)',
  license = 'MIT',
  url = 'https://github.com/yaml/pyyaml-future',

  author = 'Ingy döt Net',
  author_email = 'ingy@ingy.net',

  packages = ['yamlfuture'],
  package_dir = {'': 'lib'},
  #package_data = {
  #    '': ['ReadMe.md'],
  #},

  python_requires = '>=3.6, <4',
  install_requires = [
    'pyyaml',
  ],

  keywords = ['yaml', 'future'],
  classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3 :: Only',
  ],

  long_description = long_description,
  long_description_content_type = 'text/markdown',
  # download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',
)
