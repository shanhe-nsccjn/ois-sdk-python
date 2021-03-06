# -*- coding: utf-8 -*-

import json
import platform
import sys
import unittest

from ois.sdk import __version__
from ois.sdk.config import Config
from ois.sdk.request import Request


class SignTestCase(unittest.TestCase):

    def setUp(self):
        self.test_config = Config('ACCESS_KEY_ID', 'SECRET_ACCESS_KEY')
        self.test_op = {
            'API': 'Test',
            'Method': 'GET',
            'URI': '/<bucket-name>/<object-key>',
            'Headers': {
                'Host': 'pek3a.ois.com',
                'Date': 'Wed, 10 Dec 2014 17:20:31 GMT',
                'x-qs-test-header1': 'test',
                'x-qs-copy-source': '中文测试',
                'x-qs-fetch-source': 'https://google.com/logo.png',
                'test_empty_header': '',
            },
            'Params': {
                'test_params_1': 'test_val',
                'test_params_2': '中文测试',
                'test_params_empty': '',
            },
            'Elements': {
                'test_elements_1': 'test_val',
                'test_elements_2': '中文测试',
                'test_elements_empty': '',
            },
            'Properties': {
                'zone': 'pek3a',
                'bucket-name': 'test_bucket',
                'object-key': '中文测试.json',
            },
            'Body': None,
        }
        self.test_req = Request(self.test_config, self.test_op)

    def test_get_content_md5(self):
        content_md5 = self.test_req.get_content_md5()
        self.assertEqual(content_md5, '')

    def test_get_content_type(self):
        content_type = self.test_req.get_content_type()
        self.assertEqual(content_type, 'application/json')

    def test_get_date(self):
        date = self.test_req.get_date()
        self.assertEqual(date, 'Wed, 10 Dec 2014 17:20:31 GMT')

    def test_get_canonicalized_headers(self):
        canonicalized_headers = self.test_req.get_canonicalized_headers()
        self.assertEqual(
            canonicalized_headers,
            'x-qs-copy-source:%E4%B8%AD%E6%96%87%E6%B5%8B%E8%AF%95\n'
            'x-qs-fetch-source:https://google.com/logo.png\n'
            'x-qs-test-header1:test\n'
        )

    def test_get_canonicalized_resource(self):
        canonicalized_resource = self.test_req.get_canonicalized_resource()
        self.assertEqual(
            canonicalized_resource,
            '/test_bucket/%E4%B8%AD%E6%96%87%E6%B5%8B%E8%AF%95.json'
        )

    def test_get_authorization(self):
        authorization = self.test_req.get_authorization()
        self.assertEqual(
            authorization, 'L1Aiatm0YRH9qk8/4phJYtOlJiyHvq+ejH3sRlyUusI='
        )

    def test_get_query_signature(self):
        authorization = self.test_req.get_query_signature(100)
        self.assertEqual(
            authorization, 'y7/aT93vwQ3UMGhAnrYJCQbuu9gqj5j9kFG/4Ni/T7Q%3D'
        )

    def test_sign(self):
        req = self.test_req.sign()
        self.assertEqual(
            req.body, (
                '{'
                '"test_elements_1": "test_val", '
                '"test_elements_2": "\\u4e2d\\u6587\\u6d4b\\u8bd5", '
                '"test_elements_empty": ""'
                '}'
            )
        )
        self.assertEqual(req.headers['Content-Length'], '105')
        self.assertEqual(req.headers['Content-Type'], 'application/json')
        self.assertEqual(req.headers['Date'], 'Wed, 10 Dec 2014 17:20:31 GMT')
        self.assertEqual(req.headers['Host'], 'pek3a.ois.com')
        self.assertEqual(
            req.headers['User-Agent'], (
                'ois-sdk-python/{sdk_version}  '
                '(Python v{python_version}; {system})'
            ).format(
                sdk_version=__version__,
                python_version=platform.python_version(),
                system=sys.platform
            )
        )
        self.assertEqual(req.method, 'GET')
        self.assertEqual(
            req.url, (
                'https://pek3a.ois.com/test_bucket/'
                '%E4%B8%AD%E6%96%87%E6%B5%8B%E8%AF%95.json'
                '?test_params_1=test_val'
                '&test_params_2=%E4%B8%AD%E6%96%87%E6%B5%8B%E8%AF%95'
            )
        )

    def test_query_sign(self):
        self.maxDiff = None
        req = Request(self.test_config, self.test_op).sign_query(100)
        self.assertEqual(
            req.body, (
                '{'
                '"test_elements_1": "test_val", '
                '"test_elements_2": "\\u4e2d\\u6587\\u6d4b\\u8bd5", '
                '"test_elements_empty": ""'
                '}'
            )
        )
        self.assertEqual(req.headers['Content-Length'], '105')
        self.assertEqual(req.headers['Date'], 'Wed, 10 Dec 2014 17:20:31 GMT')
        self.assertEqual(req.headers['Host'], 'pek3a.ois.com')
        self.assertEqual(
            req.headers['User-Agent'], (
                'ois-sdk-python/{sdk_version}  '
                '(Python v{python_version}; {system})'
            ).format(
                sdk_version=__version__,
                python_version=platform.python_version(),
                system=sys.platform
            )
        )
        self.assertEqual(req.method, 'GET')
        self.assertEqual(
            req.url, (
                'https://pek3a.ois.com/test_bucket/'
                '%E4%B8%AD%E6%96%87%E6%B5%8B%E8%AF%95.json'
                '?test_params_1=test_val'
                '&test_params_2=%E4%B8%AD%E6%96%87%E6%B5%8B%E8%AF%95'
                '&signature=y7/aT93vwQ3UMGhAnrYJCQbuu9gqj5j9kFG/4Ni/T7Q%3D'
                '&access_key_id=ACCESS_KEY_ID&expires=100'
            )
        )
