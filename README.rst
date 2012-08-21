=======================
GLAMkit-url-breadcrumbs
=======================

Simple generation of Django site breadcrumbs based on the current URL path.

Documentation is available at
`Github pages <http://github.com/ixc/glamkit-url-breadcrumbs>`_ or
inside the repo.

GLAMkit-url-breadcrumbs is a part of the `GLAMkit framework <http://glamkit.org/>`_.

Dependencies
------------

 - Django

Quick Start
-----------

To get up and running quickly:

 - Download and install **GLAMkit-url-breadcrumbs** using *setup.py*, or
   a *pip* requirements file entry referencing a commit reference like::

       -e git://github.com/ixc/glamkit-url-breadcrumbs.git@60938bbd#egg=glamkit-url-breadcrumbs
 - Add ``'url_breadcrumbs'`` to INSTALLED_APPS in your settings
 - Invoke the template tag in a template. You must always provide the ``request``::

       {% load url_breadcrumbs_tags %}
       {% url_breadcrumbs request %}

By default the template tag will generate a UL/LI listing of crumb links by
converting each URL path fragment into a title-cased name, so the path
``/path-to/my_app/resource`` will be rendered as a set of links with the names
*Home > Path To > My App > Resource*.

Customization
-------------

To customize the HTML output create your own *url_breadcrumbs.html* template
file.

There are a number of ways to customize the crumb name used for URL path
components, refer to the documentation in the ``url_breadcrumbs`` template tag
for more details but common examples are:

 - In your view, set the crumb name for the current page to represent the
   resource or document being displayed::

       # Set crumb name on request object
       request.crumb = 'Full Name of This Resource'
 - In your template, override the default *Home* site root crumb name and
   the delimiter character between crumbs::

       {% with crumb_home_name="Welcome" crumb_delim="|" %}
           {% url_breadcrumbs request %}
       {% endwith %}
 - In your settings, define a list of functions as URL_BREADCRUMBS_FUNCTIONS
   to generate custom crumb names. See the included ``feincms_page_title``
   function for an example, or use this directly if your site is based
   on `FeinCMS <http://www.feincms.org/>`_::

       # Use FeinCMS page title as breadcrumb crumb name
       from url_breadcrumbs.crumb_fns import feincms_page_title
       URL_BREADCRUMBS_FUNCTIONS = [feincms_page_title]
