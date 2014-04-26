#!/usr/bin/env python
from distutils.core import setup

setup(
    name = 'bambu-blog',
    version = '0.2.4',
    description = 'A simple set of models for a basic blog, with some tools for custom-designed blog post writing',
    author = 'Steadman',
    author_email = 'mark@steadman.io',
    url = 'http://pypi.python.org/pypi/bambu-blog',
    long_description = open(path.join(path.dirname(__file__), 'README')).read(),
    install_requires = open(path.join(path.dirname(__file__), 'requirements.txt')).read().splitlines(),
    namespace_packages = ['bambu'],
    packages = [
        'bambu.blog',
        'bambu.blog.management',
        'bambu.blog.management.commands',
        'bambu.blog.migrations',
        'bambu.blog.templatetags'
    ],
    package_data = {
        'bambu.blog': [
            'templates/admin/blog/post/*.html',
            'templates/blog/*.html',
            'templates/search/indexes/blog/*.txt',
            'static/blog/*.js'
        ]
    },
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django'
    ]
)
