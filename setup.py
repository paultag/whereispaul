#!/usr/bin/env python

from whereispaul import __appname__, __version__
from setuptools import setup

long_description = open('README.rst').read()

setup(
    name       = __appname__,
    version    = __version__,
    packages   = [ 'whereispaul' ],
    author       = "Paul Tagliamonte",
    author_email = "paultag@ubuntu.com",
    long_description = long_description,
    description      = 'Talk with Google Latitude',
    license          = "BSD",
    url              = "https://github.com/paultag/whereispaul",
    platforms        = ['any']
)
