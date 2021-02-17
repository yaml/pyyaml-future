from distutils.core import setup
setup(
  name = 'pyyaml-future',
  packages = ['yamlfuture'],
  version = '0.0.1',
  license='MIT',
  description = 'Use YAML 1.3 Features in PyYAML (YAML 1.1)',
  author = 'Ingy döt Net',
  author_email = 'ingy@ingy.net',
  url = 'https://github.com/yaml/pyyaml-future',
  # download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',
  keywords = ['yaml', 'future'],
  install_requires=[
    'pyyaml',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)
