"""Packaging settings."""
from setuptools import setup
from datasetgen import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'oktopus_datasetgen',
    version = __version__,
    author="Example Author",
    author_email="author@example.com",
    description = 'Oktopus dataset generation.',
    long_description = long_description,
    long_description_content_type="text/markdown",
    url = 'https://cs-git-research.cs.surrey.sfu.ca/nsl/ISP/oktopus/dataset-gen',
    packages=['datasetgen'],
    classifiers = [
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
    ],
    entry_points = {
        'console_scripts': [
            'datasetgen=datasetgen.cli:main',
        ],
    }
)