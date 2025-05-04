from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from women.models import Women


# Create your tests here.
class GetPagesTestCase(TestCase):

    fixtures = ['women_women.json', 'women_category.json', 'women_husband.json', 'women_tagpost.json']

    def setUp(self):
        pass

    def test_main_page(self):
        path = reverse("home")
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'women/index.html')
        self.assertEqual(response.context_data['title'], "Главная страница")

    def test_redirect_add_page(self):
        path = reverse("add_page")
        redirect_url = reverse('users:login') + '?next=' + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_url)

    def test_data_main_page(self):
        w = Women.published.all().select_related('cat')
        path = reverse("home")
        response = self.client.get(path)
        self.assertQuerysetEqual(response.context_data['posts'], w[:5])

    def test_paginate_main_page(self):
        path = reverse("home")
        page = 2
        paginate_by = 5
        response = self.client.get(path + f'?page={page}&per_page={paginate_by}')
        w = Women.published.all().select_related('cat')
        self.assertQuerySetEqual(response.context_data['posts'], w[(page - 1) * paginate_by:page * paginate_by])

    def test_content_post(self):
        w = Women.published.get(pk=1)
        path = reverse("post", args=[w.slug])
        response = self.client.get(path)
        self.assertEqual(w.content, response.context_data['post'].content)

    def tearDown(self):
        pass
