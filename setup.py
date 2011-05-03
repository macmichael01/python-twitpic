#!/usr/bin/env python
#from distutils.core import setup
from setuptools import setup, find_packages


setup(name='python-twitpic',
    install_requires=('oauth',),
    description='Python TwitPic client API',
    author='Chris McMichael',
    author_email='macmichael01@gmail.com',
    url="https://github.com/macmichael01/python-twitpic",
    version='2.0',
    packages = find_packages(),
    long_description="Python TwitPic client API",
    keywords="twitpic photos tweets",
    license="BSD",
    zip_safe = True
)