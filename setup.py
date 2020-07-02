"""Packaging settings."""
import os

from setuptools import setup
from okdatasetgen import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name = 'oktopus_datasetgen',
    version = __version__,
    author='Khaled Diab, Carlos Lee',
    author_email='kdiab@sfu.ca, carlosl@sfu.ca',
    description = 'Oktopus dataset generation.',
    long_description = long_description,
    long_description_content_type='text/markdown',
    url = 'https://github.com/Oktopus-Multicast/oktopus_dataset-gen.git',
    packages=['okdatasetgen'],
    install_requires=required,
    classifiers = [
        'License :: OSI Approved :: MIT License'
    ],
    entry_points = {
        'console_scripts': [
            'okdatasetgen=okdatasetgen.cli:main',
        ],
    }
)