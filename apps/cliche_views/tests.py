import http
import json
import os

from rest_framework import test, reverse


class ClicheViewTest(test.APITestCase):
    """
    cliche view test
    """

    fixtures = [
        # 'cliche_builders.json',
        os.path.join('tests', 'cliche_builders.json'),
        os.path.join('tests', 'cliche_apps.json'),
        os.path.join('tests', 'cliche_models.json'),
        os.path.join('tests', 'cliche_schemas.json'),
        os.path.join('tests', 'cliche_views.json'),
    ]

    def test_create_cliche_view(self):
        # create new cliche model
        req_url = reverse.reverse(
            'cliche_views:cliche-views-list')
        req_data = {
            'app': '575b6eea-664c-11ee-bafb-e8f40871ee62',
            'name': 'test',
            'path': 'test1',
        }
        resp = self.client.post(
            req_url,
            data=json.dumps(req_data),
            content_type='application/json',
        )
        resp_data = resp.json()
        self.assertEqual(
            resp.status_code, http.HTTPStatus.CREATED)
        self.assertEqual(
            resp_data.get('app'),
            '575b6eea-664c-11ee-bafb-e8f40871ee62')
        self.assertEqual(resp_data.get('name'), 'test')

    def test_update_cliche_view(self):
        req_url = reverse.reverse(
            'cliche_views:cliche-views-detail',
            ['f334d4a8-8ff0-11ee-9140-e8f40871ee62'],
        )
        resp = self.client.patch(
            req_url, data={'name': 'testViewNew'})
        resp_data = resp.json()
        self.assertEqual(
            resp.status_code, http.HTTPStatus.OK)
        self.assertIsInstance(resp_data, dict)
        self.assertEqual(
            resp_data.get('uuid'),
            'f334d4a8-8ff0-11ee-9140-e8f40871ee62')
        self.assertEqual(
            resp_data.get('name'), 'testViewNew')
        self.assertEqual(
            resp_data.get('path'), 'test1/')

    def test_retrieve_cliche_view(self):
        """
        TODO: to be implemented
        """

    def test_delete_cliche_view(self):
        """
        TODO: to be implemented
        """
