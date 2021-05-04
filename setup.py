#!/usr/bin/python3

from setuptools import setup, find_packages
from codecs     import open

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='scout_debugger',
      version='2.0.0',
      description='Instruction-based research debugger (a poor man\'s debugger)',
      author='Eyal Itkin',
      author_email='eyalit@checkpoint.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/CheckPointSW/Scout',
      license='MIT',
      packages=['scout_debugger', 'scout_debugger.compilation'],
      package_dir={'scout_debugger': 'src/utils'},
      install_requires=['elementals'],
      test_requires=['pydocstyle', 'flake8', 'click'],
      classifiers=[
                    "Programming Language :: Python :: 3",
                    "License :: OSI Approved :: MIT License (MIT License)",
                    "Operating System :: OS Independent",
                  ],
      zip_safe=False)
