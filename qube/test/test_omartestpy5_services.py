#!/usr/bin/python
"""
Add docstring here
"""
import os
import time
import unittest

import mock
from mock import patch
import mongomock


with patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient):
    os.environ['OMARTESTPY5_MONGOALCHEMY_CONNECTION_STRING'] = ''
    os.environ['OMARTESTPY5_MONGOALCHEMY_SERVER'] = ''
    os.environ['OMARTESTPY5_MONGOALCHEMY_PORT'] = ''
    os.environ['OMARTESTPY5_MONGOALCHEMY_DATABASE'] = ''

    from qube.src.models.omartestpy5 import omartestpy5
    from qube.src.services.omartestpy5service import omartestpy5Service
    from qube.src.commons.context import AuthContext
    from qube.src.commons.error import ErrorCodes, omartestpy5ServiceError


class Testomartestpy5Service(unittest.TestCase):
    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def setUp(self):
        context = AuthContext("23432523452345", "tenantname",
                              "987656789765670", "orgname", "1009009009988",
                              "username", False)
        self.omartestpy5Service = omartestpy5Service(context)
        self.omartestpy5_api_model = self.createTestModelData()
        self.omartestpy5_data = self.setupDatabaseRecords(self.omartestpy5_api_model)
        self.omartestpy5_someoneelses = \
            self.setupDatabaseRecords(self.omartestpy5_api_model)
        self.omartestpy5_someoneelses.tenantId = "123432523452345"
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            self.omartestpy5_someoneelses.save()
        self.omartestpy5_api_model_put_description \
            = self.createTestModelDataDescription()
        self.test_data_collection = [self.omartestpy5_data]

    def tearDown(self):
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            for item in self.test_data_collection:
                item.remove()
            self.omartestpy5_data.remove()

    def createTestModelData(self):
        return {'name': 'test123123124'}

    def createTestModelDataDescription(self):
        return {'description': 'test123123124'}

    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def setupDatabaseRecords(self, omartestpy5_api_model):
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            omartestpy5_data = omartestpy5(name='test_record')
            for key in omartestpy5_api_model:
                omartestpy5_data.__setattr__(key, omartestpy5_api_model[key])

            omartestpy5_data.description = 'my short description'
            omartestpy5_data.tenantId = "23432523452345"
            omartestpy5_data.orgId = "987656789765670"
            omartestpy5_data.createdBy = "1009009009988"
            omartestpy5_data.modifiedBy = "1009009009988"
            omartestpy5_data.createDate = str(int(time.time()))
            omartestpy5_data.modifiedDate = str(int(time.time()))
            omartestpy5_data.save()
            return omartestpy5_data

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_post_omartestpy5(self, *args, **kwargs):
        result = self.omartestpy5Service.save(self.omartestpy5_api_model)
        self.assertTrue(result['id'] is not None)
        self.assertTrue(result['name'] == self.omartestpy5_api_model['name'])
        omartestpy5.query.get(result['id']).remove()

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_put_omartestpy5(self, *args, **kwargs):
        self.omartestpy5_api_model['name'] = 'modified for put'
        id_to_find = str(self.omartestpy5_data.mongo_id)
        result = self.omartestpy5Service.update(
            self.omartestpy5_api_model, id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))
        self.assertTrue(result['name'] == self.omartestpy5_api_model['name'])

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_put_omartestpy5_description(self, *args, **kwargs):
        self.omartestpy5_api_model_put_description['description'] =\
            'modified for put'
        id_to_find = str(self.omartestpy5_data.mongo_id)
        result = self.omartestpy5Service.update(
            self.omartestpy5_api_model_put_description, id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))
        self.assertTrue(result['description'] ==
                        self.omartestpy5_api_model_put_description['description'])

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_omartestpy5_item(self, *args, **kwargs):
        id_to_find = str(self.omartestpy5_data.mongo_id)
        result = self.omartestpy5Service.find_by_id(id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_omartestpy5_item_invalid(self, *args, **kwargs):
        id_to_find = '123notexist'
        with self.assertRaises(omartestpy5ServiceError):
            self.omartestpy5Service.find_by_id(id_to_find)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_omartestpy5_list(self, *args, **kwargs):
        result_collection = self.omartestpy5Service.get_all()
        self.assertTrue(len(result_collection) == 1,
                        "Expected result 1 but got {} ".
                        format(str(len(result_collection))))
        self.assertTrue(result_collection[0]['id'] ==
                        str(self.omartestpy5_data.mongo_id))

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_not_system_user(self, *args, **kwargs):
        id_to_delete = str(self.omartestpy5_data.mongo_id)
        with self.assertRaises(omartestpy5ServiceError) as ex:
            self.omartestpy5Service.delete(id_to_delete)
        self.assertEquals(ex.exception.errors, ErrorCodes.NOT_ALLOWED)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_by_system_user(self, *args, **kwargs):
        id_to_delete = str(self.omartestpy5_data.mongo_id)
        self.omartestpy5Service.auth_context.is_system_user = True
        self.omartestpy5Service.delete(id_to_delete)
        with self.assertRaises(omartestpy5ServiceError) as ex:
            self.omartestpy5Service.find_by_id(id_to_delete)
        self.assertEquals(ex.exception.errors, ErrorCodes.NOT_FOUND)
        self.omartestpy5Service.auth_context.is_system_user = False

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_item_someoneelse(self, *args, **kwargs):
        id_to_delete = str(self.omartestpy5_someoneelses.mongo_id)
        with self.assertRaises(omartestpy5ServiceError):
            self.omartestpy5Service.delete(id_to_delete)
