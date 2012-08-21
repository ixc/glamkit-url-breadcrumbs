#!/usr/bin/env python

import os
from setuptools import setup, find_packages

setup(
    name='glamkit-url-breadcrumbs',
    version=__import__('url_breadcrumbs').__version__,
    description=u' '.join(
        __import__('url_breadcrumbs').__doc__.splitlines()).strip(),
    long_description=os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'README.rst'),
    author='James Murty',
    author_email='james@interaction.net.au',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    url='https://github.com/ixc/glamkit-url-breadcrumbs/',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    test_suite='runtests.runtests',
)
