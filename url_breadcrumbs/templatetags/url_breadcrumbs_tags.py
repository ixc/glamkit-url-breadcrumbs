import re
import logging

from django import template
from django.conf import settings
from django.template.defaultfilters import title

register = template.Library()

re_spacify = re.compile(r'[-_+]')
log = logging.getLogger(__name__)


@register.inclusion_tag('url_breadcrumbs.html', takes_context=True)
def url_breadcrumbs(context, request):
    """
    Determine a breadcrumb trail based on the URL path of the current request.

    If no special attributes are set on request or in the context, each URL
    path slug component is automatically converted into title-cased text.
    If you're lucky enough to have a good URL path hierarchy this should be
    enough in most cases. If not, see the customization options below.

    Args:
     - ``context`` (:class:`django.template.Context`): Django request context
     - ``request`` (:class:`django.http.HttpRequest`): Django request

    Customize crumbs by setting attributes on :class:`django.http.HttpRequest`
    in your view:

     - Set ``request.crumb`` to a string value to override the name displayed
       for the current page (i.e. the last crumb)
     - Set ``request.crumbs`` to a dictionary that maps slug path components
       to string names to override an arbitrary crumb in the crumb path.
     - If the name of a crumb is set to ``None`` by either of these mechanisms,
       that crumb will be skipped

    If ``URL_BREADCRUMBS_FUNCTIONS`` in Django :mod:`django.conf.settings`
    is available, each callable item in this list will be invoked to see if
    it returns a crumb name. The callables must accept four arguments:

     - ``context`` (:class:`django.template.Context`): Django request context
     - ``request`` (:class:`django.http.HttpRequest`): Django request
     - ``path_fragment`` (unicode): Path fragment the callable will (re)name
     - ``is_current_page`` (bool): True if path fragment is for current
       page, i.e. the last page in the breadcrumbs list.

    Note that these functions are not invoked if ``request.crumb`` or
    ``request.crumbs`` is set.

    Optional :class:`template context <django.template.Context>` attributes:
     - ``crumb_home_name`` : override the name of the root Home crumb that is
       always present. Defaults to 'Home'.
     - ``crumb_delim`` : override the delimiter character rendered between
       crumb path components by the default template. Defaults to ``&raquo;``.
       Note that this value is assumed to be safe by the default template.
    """
    # Load optional context items
    crumb_home_name = context.get('crumb_home_name', 'Home')
    crumb_delim = context.get('crumb_delim', '&raquo;')

    # Split current URL path into component path items
    slug_items = [p for p in request.path.split('/') if p]
    # Always include root/Home path
    crumbs = [('/', '/', crumb_home_name)]
    for i, path_fragment in enumerate(slug_items, 1):
        is_current_page = i == len(slug_items)
        crumb_path = '/%s' % '/'.join(slug_items[:i])
        crumb_name = None
        # request.crumb attr string overrides name of current page's crumb
        if is_current_page and hasattr(request, 'crumb'):
            crumb_name = request.crumb
        # request.crumbs attr dict overrides names of arbitrary crumbs
        elif hasattr(request, 'crumbs') and path_fragment in request.crumbs:
            crumb_name = request.crumbs.get(path_fragment)
        else:
            # No explicit crumb name provided yet.

            # Check whether any callables in URL_BREADCRUMBS_FUNCTIONS give
            # us a crumb name
            try:
                for fn in settings.URL_BREADCRUMBS_FUNCTIONS:
                    crumb_name = None
                    try:
                        crumb_name = fn(context, request,
                                        path_fragment, is_current_page)
                    except:
                        # Error in crumb name generation function
                        log.warn("Crumb generation function %s failed"
                                 % fn, exc_info=True)
                    if crumb_name is not None:
                        break  # Pay attention to any non-None return value
            except AttributeError:
                # URL_BREADCRUMBS_FUNCTIONS not in settings, ignore
                pass
            except TypeError:
                # URL_BREADCRUMBS_FUNCTIONS in settings but not iterable
                log.warn("URL_BREADCRUMBS_FUNCTIONS in settings is invalid,"
                         " it cannot be iterated over. Should be a list of"
                         " callables: %s" % settings.URL_BREADCRUMBS_FUNCTIONS,
                         exc_info=True)

            # Fallback strategy is to reformat the slug component to title
            # case and hope this produces a human-friendly crumb name...
            if crumb_name is None:
                crumb_name = re_spacify.sub(' ', path_fragment)
                crumb_name = title(crumb_name)
        # If no crumb name, skip crumb entry
        if not crumb_name:
            continue
        crumbs.append((crumb_path, path_fragment, crumb_name))
    return {'crumbs': crumbs, 'crumb_delim': crumb_delim}
