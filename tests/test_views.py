# -*- coding: utf-8 -*-

from werkzeug.urls import url_quote

from fbone.user import User
from fbone.extensions import db, mail

from tests import TestCase


class TestFrontend(TestCase):

    def test_show(self):
        self._test_get_request('/', 'index.html')

    def test_footers(self):
        self._test_get_request('/help', 'frontend/footers/help.html')

class TestError(TestCase):

    def test_404(self):
        response = self.client.get('/404/')
        self.assert404(response)
        self.assertTemplateUsed('errors/page_not_found.html')
