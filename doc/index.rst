.. GLAMkit-url-breadcrumbs documentation master file, created by
   sphinx-quickstart on Wed Aug 22 09:55:45 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to GLAMkit-url-breadcrumbs's documentation!
===================================================

.. toctree::
   :maxdepth: 2

.. automodule:: url_breadcrumbs

Getting Started
---------------

To get up and running quickly:

 - Download and install **GLAMkit-url-breadcrumbs** using *setup.py*, or
   a *pip* requirements file entry referencing a commit reference like::

       -e git://github.com/ixc/glamkit-url-breadcrumbs.git@60938bbd#egg=glamkit-url-breadcrumbs
 - Add ``'url_breadcrumbs'`` to ``INSTALLED_APPS`` in your Django settings
 - Invoke the template tag in a template. You must always provide the ``request``::

       {% load url_breadcrumbs_tags %}
       {% url_breadcrumbs request %}

By default the template tag will generate a UL/LI listing of crumb links by
converting each URL path fragment into a title-cased name, so the path
``/path-to/my_app/resource`` will be rendered as a set of links with the names
*Home > Path To > My App > Resource*.

url_breadcrumbs Template Tag
----------------------------

.. automodule:: url_breadcrumbs.templatetags.url_breadcrumbs_tags
   :members:


URL_BREADCRUMBS_FUNCTIONS custom functions
------------------------------------------

.. automodule:: url_breadcrumbs.crumb_fns
   :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

