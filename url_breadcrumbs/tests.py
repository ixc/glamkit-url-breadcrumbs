from django.test import TestCase
from django.template import Context, Template
from django.test.client import RequestFactory
from django.conf import settings


class UrlBreadcrumbsTest(TestCase):

    def _build_context(self, request_path, context_items=None):
        request = self.request_factory.get(request_path)
        context_dict = {'request': request}
        if context_items is not None:
            context_dict.update(context_items)
        return Context(context_dict)

    def setUp(self):
        self.template = Template(
            "{% load url_breadcrumbs_tags %}"
            "{% url_breadcrumbs request %}"
            )
        self.request_factory = RequestFactory()
        try:
            settings.URL_BREADCRUMBS_FUNCTIONS
            settings.URL_BREADCRUMBS_FUNCTIONS = None
        except AttributeError:
            pass

    def test_render_default_context(self):
        context = self._build_context('/some-kind/of_url/path')
        html = self.template.render(context)
        self.assertTemplateUsed('breadcrumbs.html')
        # Are we using the default &raquo; delimiter?
        self.assertIn(
            '<span class="crumb-delim">&raquo;</span>', html)
        # Are we using the default name 'Home' for root crumb?
        self.assertIn(
            '<a href="/">Home</a>', html)
        # Test conversion of path components to title-cased text names
        self.assertIn(
            '<a href="/some-kind">Some Kind</a>', html)
        self.assertIn(
            '<a href="/some-kind/of_url">Of Url</a>', html)
        # Test last item in path becomes a non-link URL
        self.assertIn(
            '<span class="crumb-final">Path</span>', html)

    def test_render_alternate_home_in_context(self):
        """Override name used for root crumb"""
        context = self._build_context('/some-kind/of_url/path',
            {'crumb_home_name': 'Start Here'})
        html = self.template.render(context)
        self.assertIn(
            '<a href="/">Start Here</a>', html)

    def test_render_alternate_delimiter_in_context(self):
        """Override delimiter used between crumbs"""
        context = self._build_context('/some-kind/of_url/path',
            {'crumb_delim': '|'})
        html = self.template.render(context)
        self.assertIn(
            '<span class="crumb-delim">|</span>', html)
        # Be careful about delim content, it's treated as safe!
        context = self._build_context('/some-kind/of_url/path',
            {'crumb_delim': '<script>alert("oh noes!");</script>'})
        html = self.template.render(context)
        self.assertIn(
            '<span class="crumb-delim"><script>alert("oh noes!");</script></span>', html)

    def test_render_request_crumb_overrides(self):
        """Override crumb name of current page via request"""
        context = self._build_context('/some-kind/of_url/path',
            {'crumb_delim': '|'})
        context['request'].crumb = 'Alternate Crumb Name'
        html = self.template.render(context)
        self.assertNotIn(
            '<span class="crumb-final">Path</span>', html)
        self.assertIn(
            '<span class="crumb-final">Alternate Crumb Name</span>', html)

    def test_render_request_crumbs_overrides(self):
        """Override multiple crumb names in path via request"""
        context = self._build_context('/some-kind/of_url/path',
            {'crumb_delim': '|'})
        context['request'].crumbs = {
            'some-kind': 'Alternate Fragment Name',
            'path': 'Alternate Final Name',
            }
        html = self.template.render(context)
        self.assertIn(
            '<a href="/some-kind">Alternate Fragment Name</a>', html)
        self.assertIn(
            '<span class="crumb-final">Alternate Final Name</span>', html)

    def test_render_breadcrumb_functions_in_settings(self):
        """
        Test crumb-name generating functions in
        settings.URL_BREADCRUMBS_FUNCTIONS
        """
        context = self._build_context('/some-kind/of_url/path')
        # Returning None has no effect
        settings.URL_BREADCRUMBS_FUNCTIONS = [
            lambda ctext, req, frag, is_curr: None,
            ]
        html = self.template.render(context)
        self.assertIn(
            '<span class="crumb-final">Path</span>', html)
        # Returning empty string skips crumb
        settings.URL_BREADCRUMBS_FUNCTIONS = [
            lambda ctext, req, frag, is_curr: '' if is_curr else None,
            ]
        html = self.template.render(context)
        self.assertNotIn(
            '<span class="crumb-final">Path</span>', html)
        self.assertIn(
            '<span class="crumb-final">Of Url</span>', html)
        # Broken functions are ignored
        settings.URL_BREADCRUMBS_FUNCTIONS = [
            lambda wrong_number_of_arguments: None,
            ]
        html = self.template.render(context)
        self.assertIn(
            '<span class="crumb-final">Path</span>', html)
        # Multiple functions can be specified
        settings.URL_BREADCRUMBS_FUNCTIONS = [
            lambda ctext, req, frag, is_curr:
                'Altered 1' if frag == 'some-kind' else None,
            lambda ctext, req, frag, is_curr:
                'Altered 2' if frag == 'of_url' else None,
            # Functions processed in order
            lambda ctext, req, frag, is_curr:
                'Will Not Reach Me' if frag == 'of_url' else None
            ]
        html = self.template.render(context)
        self.assertIn(
            '<a href="/some-kind">Altered 1</a>', html)
        self.assertIn(
            '<a href="/some-kind/of_url">Altered 2</a>', html)

    def test_render_breadcrumb_functions_in_settings_for_feincms_page(self):
        """
        Test provided crumb-name generation function for extracting
        a FeinCMS page's title as the crumb name
        """
        class FakeFeinCmsPage(object):
            title = 'Title of FeinCMS Page'
        from url_breadcrumbs.crumb_fns import feincms_page_title

        context = self._build_context('/some-kind/of_url/path',
            {'feincms_page': FakeFeinCmsPage()})
        settings.URL_BREADCRUMBS_FUNCTIONS = [feincms_page_title]
        html = self.template.render(context)
        self.assertIn(
            '<span class="crumb-final">Title of FeinCMS Page</span>', html)
