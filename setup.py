#!/usr/bin/python

from setuptools import setup, find_packages
from codecs     import open

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='Scout',
      version='2.0.0',
      description='Instruction-based research debugger (a poor man\'s debugger)',
      author='Eyal Itkin',
      author_email='eyalit@checkpoint.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/CheckPointSW/Scout',
      license='MIT',
      packages=find_packages(),
      install_requires=['elementals'],
      test_requires=['pydocstyle', 'flake8', 'click'],
      classifiers=[
                    "Programming Language :: Python :: 3",
                    "License :: OSI Approved :: MIT License (MIT License)",
                    "Operating System :: OS Independent",
                  ],
      zip_safe=False)
