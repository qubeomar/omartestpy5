#!/usr/bin/python
"""
Add docstring here
"""
import time
import unittest

import mock

from mock import patch
import mongomock


class Testomartestpy5Model(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("before class")

    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def test_create_omartestpy5_model(self):
        from qube.src.models.omartestpy5 import omartestpy5
        omartestpy5_data = omartestpy5(name='testname')
        omartestpy5_data.tenantId = "23432523452345"
        omartestpy5_data.orgId = "987656789765670"
        omartestpy5_data.createdBy = "1009009009988"
        omartestpy5_data.modifiedBy = "1009009009988"
        omartestpy5_data.createDate = str(int(time.time()))
        omartestpy5_data.modifiedDate = str(int(time.time()))
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            omartestpy5_data.save()
            self.assertIsNotNone(omartestpy5_data.mongo_id)
            omartestpy5_data.remove()

    @classmethod
    def tearDownClass(cls):
        print("After class")


if __name__ == '__main__':
    unittest.main()
