import http
import json
import os
import random

from rest_framework import test, reverse


class ClicheAppTest(test.APITestCase):
    """
    test for cliche app
    """
    fixtures = [os.path.join('tests', 'cliche_apps.json')]

    def test_create_cliche_app(self):
        # create new cliche app
        req_url = reverse.reverse(
            'cliche_apps:cliche-apps-list')
        req_data = {
            'name': 'test',
            'path': 'testPrefix',
        }
        resp = self.client.post(
            req_url,
            data=json.dumps(req_data),
            content_type='application/json',
        )
        resp_data = resp.json()
        self.assertEqual(
            resp.status_code, http.HTTPStatus.CREATED)
        self.assertEqual(resp_data.get('name'), 'test')
        self.assertEqual(resp_data.get('path'), 'testPrefix')

    def test_update_cliche_app(self):
        req_url = reverse.reverse(
            'cliche_apps:cliche-apps-detail',
            ['575b6eea-664c-11ee-bafb-e8f40871ee62'],
        )
        resp = self.client.patch(
            req_url, data={'name': 'testAppNew'})
        resp_data = resp.json()
        self.assertEqual(
            resp.status_code, http.HTTPStatus.OK)
        self.assertIsInstance(resp_data, dict)
        self.assertEqual(
            resp_data.get('uuid'),
            '575b6eea-664c-11ee-bafb-e8f40871ee62')
        self.assertEqual(
            resp_data.get('name'), 'testAppNew')
        self.assertEqual(
            resp_data.get('path'), 'app1/')

    def test_retrieve_cliche_app(self):
        # retrieve all
        req_url = reverse.reverse(
            'cliche_apps:cliche-apps-list')
        resp = self.client.get(req_url)
        resp_data = resp.json()
        self.assertEqual(
            resp.status_code, http.HTTPStatus.OK)
        self.assertIsInstance(resp_data, dict)
        self.assertEqual(resp_data.get('count'), 3)
        resp_data = resp_data.get('results')
        self.assertIsInstance(resp_data, list)
        self.assertEqual(len(resp_data), 3)

        # retrieve all by name filter
        resp = self.client.get(
            req_url, data={'name_contains': '1'})
        resp_data = resp.json()
        self.assertEqual(
            resp.status_code, http.HTTPStatus.OK)
        self.assertIsInstance(resp_data, dict)
        self.assertEqual(resp_data.get('count'), 1)
        resp_data = resp_data.get('results')
        self.assertIsInstance(resp_data, list)
        self.assertEqual(len(resp_data), 1)

        # retrieve detail
        resp_data_0 = resp_data[0]
        resp_data_0_uuid = resp_data_0.get('uuid')
        self.assertIsInstance(resp_data_0_uuid, str)
        req_url = reverse.reverse(
            'cliche_apps:cliche-apps-detail',
            [resp_data_0_uuid],
        )
        resp = self.client.get(req_url)
        resp_data = resp.json()
        self.assertEqual(
            resp.status_code, http.HTTPStatus.OK)
        self.assertIsInstance(resp_data, dict)
        self.assertDictEqual(resp_data, resp_data_0)

    def test_delete_cliche_app(self):
        # delete the app successfully
        req_url = reverse.reverse(
            'cliche_apps:cliche-apps-detail',
            ['6d3903fe-664c-11ee-90bb-e8f40871ee62'],
        )
        resp = self.client.delete(req_url)
        # resp_data = resp.json()
        self.assertEqual(
            resp.status_code, http.HTTPStatus.NO_CONTENT)

        # check
        resp = self.client.get(req_url)
        self.assertEqual(
            resp.status_code, http.HTTPStatus.NOT_FOUND)

        # delete app on which is depended
        req_url = reverse.reverse(
            'cliche_apps:cliche-apps-detail',
            ['575b6eea-664c-11ee-bafb-e8f40871ee62'],
        )
        resp = self.client.delete(req_url)
        # resp_data = resp.json()
        self.assertEqual(
            resp.status_code, http.HTTPStatus.FORBIDDEN)


class ClicheAppDependencyTest(test.APITestCase):
    """
    test for cliche app dependency
    """
    fixtures = [os.path.join('tests', 'cliche_apps.json')]

    def test_create_cliche_app_dependency(self):
        req_url = reverse.reverse(
            'cliche_apps:cliche-apps-dependencies-list')

        # create new cliche app dependency successfully
        req_data = {
            'dependency': '575b6eea-664c-11ee-bafb-e8f40871ee62',
            'dependant': '6d3903fe-664c-11ee-90bb-e8f40871ee62',
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
            resp_data.get('dependency'),
            '575b6eea-664c-11ee-bafb-e8f40871ee62')
        self.assertEqual(
            resp_data.get('dependant'),
            '6d3903fe-664c-11ee-90bb-e8f40871ee62')

        # create cliche app dependency already exists
        req_data = {
            'dependency': '575b6eea-664c-11ee-bafb-e8f40871ee62',
            'dependant': '5da31300-664c-11ee-b31e-e8f40871ee62',
        }
        resp = self.client.post(
            req_url,
            data=json.dumps(req_data),
            content_type='application/json',
        )
        # resp_data = resp.json()
        self.assertEqual(
            resp.status_code, http.HTTPStatus.BAD_REQUEST)

        # create incorrect cliche app dependency
        req_data = {
            'dependency': '5da31300-664c-11ee-b31e-e8f40871ee62',
            'dependant': '575b6eea-664c-11ee-bafb-e8f40871ee62',
        }
        resp = self.client.post(
            req_url,
            data=json.dumps(req_data),
            content_type='application/json',
        )
        resp_data = resp.json()
        self.assertEqual(
            resp.status_code, http.HTTPStatus.BAD_REQUEST)
        self.assertEqual(
            resp_data.get('error_description'), 'incorrect dependencies')

    def test_update_cliche_app_dependency(self):
        req_url = reverse.reverse(
            'cliche_apps:cliche-apps-dependencies-list')
        resp = self.client.get(req_url)
        resp_data = resp.json()
        self.assertEqual(
            resp.status_code, http.HTTPStatus.OK)
        self.assertIsInstance(resp_data, dict)
        self.assertEqual(resp_data.get('count'), 2)
        resp_data = resp_data.get('results')
        self.assertIsInstance(resp_data, list)
        self.assertEqual(len(resp_data), 2)

        # not allowed to update app dependency
        req_data_uuid = resp_data[random.randint(0, 1)]['uuid']
        req_url = reverse.reverse(
            'cliche_apps:cliche-apps-dependencies-detail',
            [req_data_uuid],
        )
        resp = self.client.patch(req_url, data={
            'dependency': '575b6eea-664c-11ee-bafb-e8f40871ee62'})
        resp_data = resp.json()
        self.assertEqual(resp.status_code, http.HTTPStatus.FORBIDDEN)
        self.assertEqual(
            resp_data.get('error_description'),
            'not allowed to modify app dependencies',
        )

    # def test_retrieve_cliche_app_dependency(self):
    #     pass

    def test_delete_cliche_app_dependency(self):
        # delete app dependency successfully
        req_url = reverse.reverse(
            'cliche_apps:cliche-apps-dependencies-detail',
            ['5706af25-73cf-11ee-a603-e8f40871ee62'],
        )
        resp = self.client.delete(req_url)
        # resp_data = resp.json()
        self.assertEqual(
            resp.status_code, http.HTTPStatus.NO_CONTENT)

        # check
        resp = self.client.get(req_url)
        self.assertEqual(
            resp.status_code, http.HTTPStatus.NOT_FOUND)
