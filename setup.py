import os
from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "overlap",
    version = "0.0.1",
    author = "Andrew Quitadamo",
    author_email = "andrew.quitadamo@gmail.com",
    description = ("Script to overlap samples from multiple files"),
    license = "BSD",
    keywords = "bioinformatics",
    url = "https://github.com/shilab/sample_overlap",
    packages=['overlap'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: BSD License",
    ],
    entry_points = {
        'console_scripts': [
            'overlap = overlap.overlap:main'
        ]
    }
)
