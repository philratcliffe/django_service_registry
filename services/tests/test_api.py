"""
This module has some tests for the API.

TODO:
Coverage is minimal at the moment and many more tests should be added.

"""
import json

import requests

from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_text

from services.models import Service


class DjangoRestFrameworkTests(TestCase):
    def setUp(self):
        Service.objects.create(name='test', version='0.0.1')
        Service.objects.create(name='test', version='0.0.1')
        Service.objects.create(name='test', version='0.0.2')
        Service.objects.create(name='test', version='0.0.2')
        Service.objects.create(name='test2', version='0.0.2')
        Service.objects.create(name='test2', version='0.0.2')

        self.list_url = reverse('services_api')
        self.create_url = reverse('services_api')
        self.list_with_name_url = reverse('services_api', kwargs={'name': 'test'})
        self.list_with_name_and_version_url = reverse(
            'services_api', kwargs={
                'name': 'test',
                'version': '0.0.1'
            })

    def test_list(self):
        response = self.client.get(self.list_url)

        self.assertContains(response, 'test2')
        self.assertContains(response, '0.0.1')
        self.assertContains(response, '0.0.2')
        self.assertEquals(response.status_code, 200)
        data = json.loads(force_text(response.content))
        self.assertEquals(len(data), 6)

    def test_list_with_name(self):
        response = self.client.get(self.list_with_name_url)
        self.assertEquals(response.status_code, 200)
        data = json.loads(force_text(response.content))
        self.assertEquals(len(data), 2)

    def test_list_with_name_and_version(self):
        response = self.client.get(self.list_with_name_and_version_url)
        self.assertEquals(response.status_code, 200)
        data = json.loads(force_text(response.content))
        self.assertEquals(len(data), 3)
        expected_data = {'name':'test', 'version':'0.0.1', 'count':2 }
        self.assertEqual(data, expected_data)
