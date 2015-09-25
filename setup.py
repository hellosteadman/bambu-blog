#!/usr/bin/env python
from setuptools import setup
from os import path

setup(
    name = 'bambu-blog',
    version = '3.3.1',
    description = 'A simple set of models for a basic blog, with some tools for custom-designed blog post writing',
    author = 'Steadman',
    author_email = 'mark@steadman.io',
    url = 'https://github.com/iamsteadman/bambu-blog',
    long_description = open(path.join(path.dirname(__file__), 'README')).read(),
    install_requires = [
        'Django>=1.8',
        'pyquery',
        'html2text',
        'django-taggit',
        'sorl-thumbnail',
        'bambu-markup>=3.0',
        'bambu-oembed>=3.0',
        'bambu-attachments>=3.0',
        'bambu-xmlrpc>=3.0'
    ],
    packages = [
        'bambu_blog',
        'bambu_blog.management',
        'bambu_blog.management.commands',
        'bambu_blog.migrations',
        'bambu_blog.templatetags'
    ],
    package_data = {
        'bambu_blog': [
            'templates/blog/*.html',
            'templates/search/indexes/bambu_blog/*.txt',
            'static/blog/*.js'
        ]
    },
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django'
    ]
)
