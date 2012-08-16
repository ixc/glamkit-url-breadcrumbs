from django.test import TestCase
from django.template import Context, Template, Request


class UrlBreadcrumbsTest(TestCase):

    def setUp(self):
        self.template = Template(
            "{% load url_breadcrumbs %}"
            "{{ url_breadcrumbs request }}"
            )
        self.context = Context({})
        self.request = Request()

    def test_render_default_context(self):
        html = self.template.render(self.context, self.request)
        self.assertEqual("TODO", html)

    def test_render_alternate_home_in_context(self):
        pass  # TODO

    def test_render_alternate_delimiter_in_context(self):
        pass  # TODO

    def test_render_request_crumb_overrides(self):
        pass  # TODO

    def test_render_request_crumbs_overrides(self):
        pass  # TODO

    def test_render_breadcrumb_functions_in_settings(self):
        pass  # TODO
