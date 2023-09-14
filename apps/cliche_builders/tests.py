import http
import json
import os

from rest_framework import test, reverse


class ClicheBuilderTargetTest(test.APITestCase):
    """
    cliche build target test
    """

    fixtures = [os.path.join('tests', 'cliche_builders.json')]

    # def test_create_cliche_build_target(self):
    #     # create new cliche build target
    #     req_url = reverse.reverse(
    #         'cliche_builders:cliche-builders-targets-list')
    #     req_data = {
    #         'name': 'test',
    #         'description': 'test desc',
    #         'code': '...',
    #     }
    #     resp = self.client.post(
    #         req_url,
    #         data=json.dumps(req_data),
    #         content_type='application/json',
    #     )
    #     resp_data = resp.json()
    #     self.assertEqual(
    #         resp.status_code, http.HTTPStatus.CREATED)
    #     self.assertEqual(resp_data.get('name'), 'test')
    #     self.assertEqual(resp_data.get('description'), 'test desc')
    #     self.assertEqual(resp_data.get('code'), '...')

    # def test_update_cliche_build_target(self):
    #     req_url = reverse.reverse(
    #         'cliche_builders:cliche-builders-targets-detail',
    #         ['testDjango'],
    #     )
    #     resp = self.client.patch(req_url, data={
    #         'name': 'testTarget',
    #         'description': 'test test for Django framework'
    #     })
    #     resp_data = resp.json()
    #     self.assertEqual(
    #         resp.status_code, http.HTTPStatus.OK)
    #     self.assertIsInstance(resp_data, dict)
    #     # name won't be changed
    #     self.assertEqual(
    #         resp_data.get('name'), 'testDjango')
    #     self.assertEqual(
    #         resp_data.get('description'),
    #         'test test for Django framework'
    #     )

    def test_retrieve_cliche_build_target(self):
        # retrieve all
        req_url = reverse.reverse(
            'cliche_builders:cliche-builders-targets-list')
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
            req_url, data={'name_contains': 'Django'})
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
        resp_data_0_name = resp_data_0.get('name')
        self.assertIsInstance(resp_data_0_name, str)
        req_url = reverse.reverse(
            'cliche_builders:cliche-builders-targets-detail',
            [resp_data_0_name],
        )
        resp = self.client.get(req_url)
        resp_data = resp.json()
        self.assertEqual(
            resp.status_code, http.HTTPStatus.OK)
        self.assertIsInstance(resp_data, dict)
        self.assertDictEqual(resp_data, resp_data_0)

    # def test_delete_cliche_build_target(self):
    #     # delete build target with error
    #     req_url = reverse.reverse(
    #         'cliche_builders:cliche-builders-targets-detail',
    #         ['testDjango'],
    #     )
    #     resp = self.client.delete(req_url)
    #     self.assertEqual(
    #         resp.status_code, http.HTTPStatus.FORBIDDEN)
    #
    #     # delete build target
    #     req_url = reverse.reverse(
    #         'cliche_builders:cliche-builders-targets-detail',
    #         ['testCliche'],
    #     )
    #     resp = self.client.delete(req_url)
    #     # resp_data = resp.json()
    #     self.assertEqual(resp.status_code, http.HTTPStatus.NO_CONTENT)
    #
    #     # check
    #     resp = self.client.get(req_url)
    #     self.assertEqual(resp.status_code, http.HTTPStatus.NOT_FOUND)


class ClicheBuilderTest(test.APITestCase):
    """
    cliche builder test
    """

    fixtures = [os.path.join('tests', 'cliche_builders.json')]

    def test_create_cliche_builder(self):
        # create new cliche builder
        req_url = reverse.reverse(
            'cliche_builders:cliche-builders-list')
        req_data_settings = {'a': '...'}
        req_data = {
            'name': 'newTestBuilder',
            'target': 'testBeego',
            'settings': req_data_settings,
        }
        resp = self.client.post(
            req_url,
            data=json.dumps(req_data),
            content_type='application/json',
        )
        resp_data = resp.json()
        self.assertEqual(resp.status_code, http.HTTPStatus.CREATED)
        self.assertEqual(resp_data.get('name'), 'newTestBuilder')
        self.assertEqual(resp_data.get('target'), 'testBeego')
        self.assertDictEqual(resp_data.get('settings'), req_data_settings)

    def test_update_cliche_builder(self):
        # test update cliche builder
        req_url = reverse.reverse(
            'cliche_builders:cliche-builders-detail',
            ['e5483eda-69c8-11ee-90a9-ba4b1618bd03'],
        )
        req_data = {
            'name': 'updatedTestBuilder',
            'target': 'testCliche',
        }
        resp = self.client.patch(
            req_url,
            data=json.dumps(req_data),
            content_type='application/json',
        )
        resp_data = resp.json()
        self.assertEqual(resp.status_code, http.HTTPStatus.OK)
        self.assertEqual(resp_data.get('name'), 'updatedTestBuilder')
        # target will not be changed
        self.assertEqual(resp_data.get('target'), 'testDjango')

    def test_retrieve_cliche_builder(self):
        # retrieve all
        req_url = reverse.reverse(
            'cliche_builders:cliche-builders-list')
        resp = self.client.get(req_url)
        resp_data = resp.json()
        self.assertEqual(
            resp.status_code, http.HTTPStatus.OK)
        self.assertIsInstance(resp_data, dict)
        self.assertEqual(resp_data.get('count'), 2)
        resp_data = resp_data.get('results')
        self.assertIsInstance(resp_data, list)
        self.assertEqual(len(resp_data), 2)

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

        # retrieve all by target
        resp = self.client.get(req_url, data={
            'target': 'testDjango'})
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
            'cliche_builders:cliche-builders-detail',
            [resp_data_0_uuid],
        )
        resp = self.client.get(req_url)
        resp_data = resp.json()
        self.assertEqual(
            resp.status_code, http.HTTPStatus.OK)
        self.assertIsInstance(resp_data, dict)
        self.assertDictEqual(resp_data, resp_data_0)

    def test_delete_cliche_builder(self):
        # delete build target
        req_url = reverse.reverse(
            'cliche_builders:cliche-builders-detail',
            ['c15004b2-69c9-11ee-90a9-ba4b1618bd03'],
        )
        resp = self.client.delete(req_url)
        # resp_data = resp.json()
        self.assertEqual(resp.status_code, http.HTTPStatus.NO_CONTENT)

        # check
        resp = self.client.get(req_url)
        self.assertEqual(resp.status_code, http.HTTPStatus.NOT_FOUND)


class ClicheBuilderBuildToDjango3Test(test.APITestCase):
    """
    cliche builder build test
    """

    fixtures = [
        'cliche_models.json',
        'cliche_schemas.json',
        os.path.join('tests', 'cliche_apps.json'),
        os.path.join('tests', 'cliche_models.json'),
        os.path.join('tests', 'cliche_schemas.json'),
        os.path.join('tests', 'cliche_views.json'),
        os.path.join('targets', 'Django-3', 'dist.json'),
    ]

    def test_build(self):
        # try to build for Django-3 ---------------------------------
        # set view with script --------------------------------------
        req_url = reverse.reverse(
            'cliche_views:cliche-views-methods-scripts-list'
        )
        resp = self.client.post(req_url, data={
            'target': 'Django-3',
            'method': 'df897b01-9416-11ee-a9a5-e8f40871ee62',
            'script': '025485e0-ac47-11ee-b0c9-ba4b1618bd02',
        })
        self.assertEqual(
            resp.status_code, http.HTTPStatus.CREATED)

        resp = self.client.post(req_url, data={
            'target': 'Django-3',
            'method': 'f03a3546-9416-11ee-b6d5-e8f40871ee62',
            'script': '0054630a-ac47-11ee-b0c9-ba4b1618bd02',
        })
        self.assertEqual(
            resp.status_code, http.HTTPStatus.CREATED)

        # add build config ------------------------------------------
        req_url = reverse.reverse(
            'cliche_builders:cliche-builders-list')
        req_data = {
            "name": "testBuilder3",
            "directory": "dist",
            'target': 'Django-3',
            "requirements": {
                "Django": "3.2.3"
            },
            'settings': {
                "INSTALLED_APPS": [
                    "django.contrib.admin",
                    "django.contrib.auth",
                    "django.contrib.contenttypes",
                    "django.contrib.sessions",
                    "django.contrib.messages",
                    "django.contrib.staticfiles"
                ]
            },
        }
        resp = self.client.post(
            req_url,
            data=json.dumps(req_data),
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, http.HTTPStatus.CREATED)
        resp_data = resp.json()
        resp_uuid = resp_data['uuid']

        # start building --------------------------------------------
        req_url = reverse.reverse(
            'cliche_builders:cliche-builders-build', [resp_uuid])
        resp = self.client.post(req_url)
        resp_data = resp.json()
        print(resp_data)
        self.assertEqual(resp.status_code, http.HTTPStatus.OK)
        self.assertDictEqual(resp_data, {'error': 'Build Succeed'})
