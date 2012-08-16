import re

from django import template, settings
from django.template.defaultfilters import title

register = template.Library()

re_spacify = re.compile(r'[-_+]')


@register.inclusion_tag('url_breadcrumbs/breadcrumbs.html', takes_context=True)
def url_breadcrumbs(context, request):
    """
    Determine a breadcrumb trail based on the URL path of the current request.

    If no special attributes are set on request or in the context, each URL
    path slug component is automatically converted into title-cased text.
    If you're lucky enough to have a good URL path hierarchy this should be
    enough in most cases.

    Optional request attributes:
     - Set `request.crumb` to a string value to override the name displayed for
       the current page (i.e. the last crumb)
     - Set `request.crumbs` to a dictionary that maps slug path components to
       string names to override an arbitrary crumb in the crumb path.
     - If the name of a crumb is set to None by either of these mechanisms,
       that crumb will be skipped

    If the URL_BREADCRUMBS_FUNCTIONS Django setting is available, each callable
    item in this list will be invoked to see if it returns a crumb name.
    Note that these functions are not invoked if `request.crumb` or
    `request.crumbs` is set.

    Optional context attributes:
     - `crumb_home_name` : override the name of the root Home crumb that is
       always present. Defaults to 'Home'.
     - `crumb_delim` : override the delimiter character rendered between crumb
       path components by the default template. Defaults to '&raquo;'.
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
            if hasattr(settings, 'URL_BREADCRUMBS_FUNCTIONS'):
                for fn in settings.URL_BREADCRUMBS_FUNCTIONS:
                    crumb_name = fn(context, request,
                                    path_fragment, is_current_page)
                    if crumb_name is not None:
                        break  # Pay attention to any non-None return value

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
