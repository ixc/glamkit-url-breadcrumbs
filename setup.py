#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='glamkit-url-breadcrumbs',
    version='0.1.0',
    description='Django site breadcrumbs based on the URL path',
    author='James Murty',
    author_email='james@interaction.net.au',
    url='http://glamkit.org/',
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
