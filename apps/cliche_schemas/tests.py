import http
import json
import os

from rest_framework import test, reverse


class ClicheSchemaTest(test.APITestCase):
    """
    cliche schema test
    """
    fixtures = [
        'cliche_schemas.json',
        os.path.join('tests', 'cliche_apps.json'),
        os.path.join('tests', 'cliche_schemas.json'),
    ]

    def test_create_cliche_schema(self):
        # create new cliche model
        req_url = reverse.reverse(
            'cliche_schemas:cliche-schemas-list')
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

    def test_update_cliche_schema(self):
        req_url = reverse.reverse(
            'cliche_schemas:cliche-schemas-detail',
            ['b8ad65c6-7ec8-11ee-9bb8-e8f40871ee62'],
        )
        resp = self.client.patch(
            req_url, data={'name': 'testSchemaNew'})
        resp_data = resp.json()
        self.assertEqual(
            resp.status_code, http.HTTPStatus.OK)
        self.assertIsInstance(resp_data, dict)
        self.assertEqual(
            resp_data.get('uuid'),
            'b8ad65c6-7ec8-11ee-9bb8-e8f40871ee62')
        self.assertEqual(
            resp_data.get('name'), 'testSchemaNew')
        resp_data_attrs = resp_data.get('attributes')
        self.assertIsInstance(resp_data_attrs, dict)
        self.assertDictEqual(resp_data_attrs, {})

    def test_retrieve_cliche_schema(self):
        req_url = reverse.reverse(
            'cliche_schemas:cliche-schemas-detail',
            ['b8ad65c6-7ec8-11ee-9bb8-e8f40871ee62'],
        )
        resp = self.client.patch(
            req_url, data={'name': 'testSchemaNew'})
        resp_data = resp.json()
        self.assertEqual(
            resp.status_code, http.HTTPStatus.OK)
        self.assertIsInstance(resp_data, dict)
        self.assertEqual(
            resp_data.get('uuid'),
            'b8ad65c6-7ec8-11ee-9bb8-e8f40871ee62')
        self.assertEqual(
            resp_data.get('name'), 'testSchemaNew')
        resp_data_attrs = resp_data.get('attributes')
        self.assertIsInstance(resp_data_attrs, dict)
        self.assertDictEqual(resp_data_attrs, {})

    def test_delete_cliche_schema(self):
        # delete the 1st model
        req_url = reverse.reverse(
            'cliche_schemas:cliche-schemas-detail',
            ['b8ad65c6-7ec8-11ee-9bb8-e8f40871ee62'],
        )
        resp = self.client.delete(req_url)
        # resp_data = resp.json()
        self.assertEqual(
            resp.status_code, http.HTTPStatus.NO_CONTENT)

        # check
        resp = self.client.get(req_url)
        self.assertEqual(
            resp.status_code, http.HTTPStatus.NOT_FOUND)


class ClicheSchemaFieldTest(test.APITestCase):
    """
    cliche schema field test
    """
    fixtures = [
        'cliche_schemas.json',
        os.path.join('tests', 'cliche_apps.json'),
        os.path.join('tests', 'cliche_schemas.json'),
    ]

    def test_create_cliche_schema_field(self):
        req_url = reverse.reverse(
            'cliche_schemas:cliche-schemas-fields-list')

        # create uuid field with serializerForeign
        req_data = {
            'schema': 'b8ad65c6-7ec8-11ee-9bb8-e8f40871ee62',
            'schema_nested': 'b8ad65c6-7ec8-11ee-9bb8-e8f40871ee62',
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
            'foreign schema should be null',
        )

        # create uuid field successfully
        req_data = {
            'schema': 'b8ad65c6-7ec8-11ee-9bb8-e8f40871ee62',
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
            resp_data.get('schema'),
            'b8ad65c6-7ec8-11ee-9bb8-e8f40871ee62')
        self.assertEqual(resp_data.get('name'), 'testID')

        # create serializer without serializerForeign
        req_data = {
            'schema': 'b8ad65c6-7ec8-11ee-9bb8-e8f40871ee62',
            'name': 'testSchema',
            'type': 'Nested',
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
            'foreign schema not specified',
        )

        # create foreign key successfully
        req_data = {
            'schema': 'c1cb4388-7ec8-11ee-acee-e8f40871ee62',
            'schema_nested': 'c1cb4388-7ec8-11ee-acee-e8f40871ee62',
            'name': 'testSchema',
            'type': 'Nested',
            'attributes': {},
        }
        resp = self.client.post(
            req_url,
            data=json.dumps(req_data),
            content_type='application/json',
        )
        # resp_data = resp.json()
        self.assertEqual(
            resp.status_code, http.HTTPStatus.CREATED)

    def test_update_cliche_schema_field(self):
        pass

    def test_retrieve_cliche_schema_field(self):
        pass

    def test_delete_cliche_schema_field(self):
        pass
