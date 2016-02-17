from __future__ import absolute_import
import os

from django.test import TestCase
from django.test.utils import override_settings
from django.conf import settings

from django.template import Context
from django.template.loader import get_template

TESTS_ROOT = os.path.dirname(os.path.abspath(__file__))
TESTS_TEMPLATE_DIR = os.path.join(TESTS_ROOT, 'templates')
TESTS_TEMPLATE_DIRS = settings.TEMPLATE_DIRS + [TESTS_TEMPLATE_DIR]

TESTS_TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [os.path.join(TESTS_ROOT, 'templates')],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

@override_settings(TEMPLATE_DIRS=TESTS_TEMPLATE_DIRS,
                   TEMPLATES=TESTS_TEMPLATES,
                   PREMAILER_OPTIONS=dict(base_url='http://example.com'))
class PremailerTests(TestCase):

    def assert_expected(self, actual, expected):
        with open(os.path.join(TESTS_TEMPLATE_DIR, expected), 'r') as f:
            self.assertEqual(actual, f.read())

    def test_basic(self):
        """
        A very basic test that ensures the tag does what we expect it to do.
        """
        template = get_template('basic.html')
        rendered = template.render(Context({'eggs': 'Sausage'}))
        self.assert_expected(rendered, 'basic.expected.html')

    def test_basic_base_url(self):
        """
        Override the base_url.
        """
        template = get_template('basic-base-url.html')
        rendered = template.render(Context({'eggs': 'Sausage'}))
        self.assert_expected(rendered, 'basic-base-url.expected.html')
