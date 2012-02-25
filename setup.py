#!/usr/bin/env python
from distutils.core import setup
from setuptools import find_packages


setup(name='python-twitpic',
    install_requires=('oauth',),
    description='Python TwitPic Client API',
    author='Chris McMichael',
    author_email='macmichael01@gmail.com',
    url="https://github.com/macmichael01/python-twitpic",
    version='2.1',
    packages = find_packages(),
	scripts=['script/twitpic'],
    long_description="Python TwitPic Client API",
    keywords="twitpic photos tweets",
    license="BSD"
)