#!/usr/bin/env python
# Based on example at https://github.com/mlavin/django-app-template
import sys
import logging

from django.conf import settings


logging.basicConfig(level=logging.ERROR)


if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=(
            'url_breadcrumbs',
        ),
        SITE_ID=1,
        SECRET_KEY='secret_key',
    )


from django.test.utils import get_runner


def runtests():
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(['url_breadcrumbs', ])
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
