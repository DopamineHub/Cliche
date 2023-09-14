import http
import json
import os

from rest_framework import test, reverse


class ClicheModelTest(test.APITestCase):
    """
    cliche model test
    """

    fixtures = [
        'cliche_models.json',
        os.path.join('tests', 'cliche_apps.json'),
        os.path.join('tests', 'cliche_models.json'),
    ]

    def test_create_cliche_model(self):
        # create new cliche model
        req_url = reverse.reverse(
            'cliche_models:cliche-models-list')
        req_data = {
            'app': '575b6eea-664c-11ee-bafb-e8f40871ee62',
            'name': 'test',
            'attributes': {},
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

    def test_update_cliche_model(self):
        req_url = reverse.reverse(
            'cliche_models:cliche-models-detail',
            ['9acf0927-67da-11ee-8a23-e8f40871ee62'],
        )
        resp = self.client.patch(
            req_url, data={'name': 'testModelNew'})
        resp_data = resp.json()
        self.assertEqual(
            resp.status_code, http.HTTPStatus.OK)
        self.assertIsInstance(resp_data, dict)
        self.assertEqual(
            resp_data.get('uuid'),
            '9acf0927-67da-11ee-8a23-e8f40871ee62')
        self.assertEqual(
            resp_data.get('name'), 'testModelNew')
        resp_data_attrs = resp_data.get('attributes')
        self.assertIsInstance(resp_data_attrs, dict)
        self.assertDictEqual(resp_data_attrs, {})

    def test_retrieve_cliche_model(self):
        # retrieve all
        req_url = reverse.reverse(
            'cliche_models:cliche-models-list')
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
            'cliche_models:cliche-models-detail',
            [resp_data_0_uuid],
        )
        resp = self.client.get(req_url)
        resp_data = resp.json()
        self.assertEqual(
            resp.status_code, http.HTTPStatus.OK)
        self.assertIsInstance(resp_data, dict)
        self.assertDictEqual(resp_data, resp_data_0)

    def test_delete_cliche_model(self):
        # delete the 1st model
        req_url = reverse.reverse(
            'cliche_models:cliche-models-detail',
            ['9acf0927-67da-11ee-8a23-e8f40871ee62'],
        )
        resp = self.client.delete(req_url)
        # resp_data = resp.json()
        self.assertEqual(
            resp.status_code, http.HTTPStatus.NO_CONTENT)

        # check
        resp = self.client.get(req_url)
        self.assertEqual(
            resp.status_code, http.HTTPStatus.NOT_FOUND)


class ClicheModelFieldTest(test.APITestCase):
    """
    cliche model field test
    """

    fixtures = [
        'cliche_models.json',
        os.path.join('tests', 'cliche_apps.json'),
        os.path.join('tests', 'cliche_models.json'),
    ]

    def test_create_cliche_model_field(self):
        req_url = reverse.reverse(
            'cliche_models:cliche-models-fields-list')

        # create uuid field with modelForeign
        req_data = {
            'model': 'bb8b0e13-67da-11ee-abce-e8f40871ee62',
            'model_foreign': 'bb8b0e13-67da-11ee-abce-e8f40871ee62',
            'name': 'testID',
            'type': 'UUID',
            'attributes': {},
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
            resp_data.get('error_description'),
            'foreign key should be null',
        )

        # create uuid field successfully
        req_data = {
            'model': 'bb8b0e13-67da-11ee-abce-e8f40871ee62',
            'name': 'testID',
            'type': 'UUID',
            'attributes': {},
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
            resp_data.get('model'),
            'bb8b0e13-67da-11ee-abce-e8f40871ee62')
        self.assertEqual(resp_data.get('name'), 'testID')

        # create foreign key without modelForeign
        req_data = {
            'model': 'bb8b0e13-67da-11ee-abce-e8f40871ee62',
            'name': 'testForeign',
            'type': 'ForeignKey',
            'attributes': {},
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
            resp_data.get('error_description'),
            'foreign key not specified',
        )

        # create foreign key successfully
        req_data = {
            'model': 'b3f02904-67da-11ee-82ad-e8f40871ee62',
            'model_foreign': 'bb8b0e13-67da-11ee-abce-e8f40871ee62',
            'name': 'testForeign',
            'type': 'ForeignKey',
            'attributes': {},
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
            str(resp_data.get('model_foreign')),
            'bb8b0e13-67da-11ee-abce-e8f40871ee62',
        )

    def test_update_cliche_model_field(self):
        pass

    def test_retrieve_cliche_model_field(self):
        pass

    def test_destroy_cliche_model_field(self):
        pass
