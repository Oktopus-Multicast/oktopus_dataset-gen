"""Packaging settings."""
from setuptools import setup
from okdatasetgen import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

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
    classifiers = [
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License'
    ],
    entry_points = {
        'console_scripts': [
            'okdatasetgen=okdatasetgen.cli:main',
        ],
    }
)