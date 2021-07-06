# -*- coding: utf-8 -*-

import json
from os import path

import yaml
from assertpy import assert_that
from behave import *

from ois.sdk.config import Config
from ois.sdk.service.ois import OIS

test_config_file_path = path.abspath(
    path.join(path.dirname(__file__), path.pardir)
)
config = Config(
).load_config_from_filepath(test_config_file_path + "/config.yaml")
ois = OIS(config)
with open(test_config_file_path + '/test_config.yaml') as f:
    test = yaml.load(f)
    f.close()
bucket = ois.Bucket(test['bucket_name'], test['zone'])
bucket.put()


@when(u'put bucket ACL')
def step_impl(context):
    context.res = bucket.put_acl(json.loads(context.text)['acl'])


@then(u'put bucket ACL status code is 200')
def step_impl(context):
    assert_that(context.res.status_code).is_equal_to(200)


@when(u'get bucket ACL')
def step_impl(context):
    context.res = bucket.get_acl()


@then(u'get bucket ACL status code is 200')
def step_impl(context):
    assert_that(context.res.status_code).is_equal_to(200)


@then(u'get bucket ACL should have grantee name "QS_ALL_USERS"')
def step_impl(context):
    ok = False
    for i in context.res['acl']:
        if i['grantee']['name'] == 'QS_ALL_USERS':
            ok = True
    assert_that(ok).is_equal_to(True)
