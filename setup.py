# -*- coding: utf-8 -*-

from setuptools import setup

project = "polichart"

setup(
    name=project,
    version='0.2',
    url='https://github.com/cjmabry/PoliChart',
    description='Election projections, data visualization, and political rants.',
    author='Chris Mabry',
    author_email='cjmab28@gmail.com',
    packages=["polichart"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask>=0.10.1',
        'Flask-SQLAlchemy',
        'Flask-WTF',
        'Flask-Script',
        'Flask-Babel',
        'Flask-Testing',
        'Flask-Mail',
        'Flask-Cache',
        'Flask-Login',
        'Flask-OpenID',
        'nose',
        'mysql-python',
        'fabric',
    ],
    test_suite='tests',
    classifiers=[
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ]
)
