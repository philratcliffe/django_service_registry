"""
This module has some tests for the API.

TODO:
Coverage is minimal at the moment and many more tests should be added.
"""

__author__ = 'Phil Ratcliffe'

import json

from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_text

from services.models import Service


class DjangoRestFrameworkTests(TestCase):
    def setUp(self):
        Service.objects.create(service='test', version='0.0.1')
        Service.objects.create(service='test', version='0.0.1')
        Service.objects.create(service='test', version='0.0.2')
        Service.objects.create(service='test', version='0.0.2')
        Service.objects.create(service='test2', version='0.0.2')
        Service.objects.create(service='test2', version='0.0.2')

        #
        # Create the URLs we will use in the tests
        #
        self.list_url = reverse('list_or_add_endpoint')
        self.add_url = reverse('list_or_add_endpoint')
        self.non_existing_service_url = reverse(
            'find_or_delete_endpoint', kwargs={
                'service': 'notaservicename'
            })
        self.delete_url = reverse(
            'find_or_delete_endpoint', kwargs={
                'service': 'test'
            })
        self.find_with_service_url = reverse(
            'find_or_delete_endpoint', kwargs={
                'service': 'test'
            })
        self.find_with_service_and_version_url = reverse(
            'find_or_delete_endpoint',
            kwargs={
                'service': 'test',
                'version': '0.0.1'
            })
        self.find_non_existing_with_service_and_version_url = reverse(
            'find_or_delete_endpoint',
            kwargs={
                'service': 'test',
                'version': '0.0.4'
            })
        self.update_url = reverse('update_endpoint', kwargs={'pk': '1'})

    def test_list(self):
        response = self.client.get(self.list_url)

        self.assertContains(response, 'test2')
        self.assertContains(response, '0.0.1')
        self.assertContains(response, '0.0.2')
        self.assertEquals(response.status_code, 200)
        data = json.loads(force_text(response.content))
        self.assertEquals(len(data), 6)
        expected_data = [
            {
                "service": "test",
                "version": "0.0.1"
            },
            {
                "service": "test",
                "version": "0.0.1"
            },
            {
                "service": "test",
                "version": "0.0.2"
            },
            {
                "service": "test",
                "version": "0.0.2"
            },
            {
                "service": "test2",
                "version": "0.0.2"
            },
            {
                "service": "test2",
                "version": "0.0.2"
            },
        ]
        self.assertEqual(data, expected_data)

    def test_find_service_with_service(self):
        response = self.client.get(self.find_with_service_url)
        self.assertEquals(response.status_code, 200)
        data = json.loads(force_text(response.content))
        self.assertEquals(len(data), 2)

    def test_add_service(self):
        post_data = {'service': 'test', 'version': '0.0.3'}
        response = self.client.post(self.add_url, post_data, format='json')
        self.assertEquals(response.status_code, 201)
        response_data = json.loads(force_text(response.content))
        self.assertEquals(len(response_data), 3)
        expected_data = {
            'service': 'test',
            'version': '0.0.3',
            'change': 'created'
        }
        self.assertEqual(response_data, expected_data)

    def test_find_service_with_service_and_version(self):
        response = self.client.get(self.find_with_service_and_version_url)
        self.assertEquals(response.status_code, 200)
        data = json.loads(force_text(response.content))
        self.assertEquals(len(data), 3)
        expected_data = {'service': 'test', 'version': '0.0.1', 'count': 2}
        self.assertEqual(data, expected_data)

    def test_find_non_existing_service_with_service_and_version(self):
        response = self.client.get(
            self.find_non_existing_with_service_and_version_url)
        self.assertEquals(response.status_code, 200)
        data = json.loads(force_text(response.content))
        self.assertEquals(len(data), 3)
        expected_data = {'service': 'test', 'version': '0.0.4', 'count': 0}
        self.assertEqual(data, expected_data)

    def test_remove_service(self):
        response = self.client.delete(self.delete_url)
        self.assertEquals(response.status_code, 200)
        data = json.loads(force_text(response.content))
        expected_data = {'service': 'test', 'change': 'removed'}
        self.assertEqual(data, expected_data)

    def test_remove_non_existing_service(self):
        response = self.client.delete(self.non_existing_service_url)
        self.assertEquals(response.status_code, 404)
        data = json.loads(force_text(response.content))
        expected_data = {'error': 'not found'}
        self.assertEqual(data, expected_data)

    def test_update_service(self):
        response = self.client.put(self.update_url, {
            'service': 'testu',
            'version': '0.0.9'
        })
