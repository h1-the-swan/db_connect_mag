# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='db_connect_mag',
    version='0.1.0',
    description='Connect to custom (local) MySQL database for Microsoft Academic Graph data',
    long_description=readme,
    author='Jason Portenoy',
    author_email='jason.portenoy@gmail.com',
    url='https://github.com/h1-the-swan/db_connect_mag.git',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=['sqlalchemy']
)

