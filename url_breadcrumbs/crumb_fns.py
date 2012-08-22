"""
Helper functions for the
:mod:`url_breadcrumbs.templatetags.url_breadcrumbs_tags` template tag.

Configure the template tag to call these helper functions, or functions of
your own, by defining ``URL_BREADCRUMBS_FUNCTIONS`` in your Django 
:mod:`django.conf.settings` and setting the value to a list of one or more
callables.

Each callable in the ``URL_BREADCRUMBS_FUNCTIONS`` setting must accept three
arguments:

 - context : the template context
 - request : the current request
 - path_fragment (str): the URL path component being converted into a crumb name
 - is_current_page (bool): ``True`` if the path fragment is for the current
   page, ``False`` if it is for any ancestor pages.

The callables must return one of the following:
 - ``None`` if they do not wish to set the crumb name
 - Empty string if the path fragment should not appear in the breadcrumb
 - String name for the crumb representing the path fragment
"""


def feincms_page_title(context, request, path_fragment, is_current_page):
    """
    Set the crumb name to the title of the current FeinCMS page, if one is
    available in the current context.
    """
    # We only want to set the crumb title for the current page
    if not is_current_page:
        return None
    # If a FeinCMS page with a title is set in the context, use as crumb name
    if 'feincms_page' in context and hasattr(context['feincms_page'], 'title'):
        return context['feincms_page'].title
    # If no titled FeinCMS page is available leave template tag to figure out
    # an appropriate crumb name
    return None
