# -*- coding: utf-8 -*-

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
with open("scenarios/features/fixtures/test.jpg", "rb") as f:
    bucket.put_object("test.jpg", body=f)


@when(u'image process with key "{key}" and query "{query}"')
def step_impl(context, key, query):
    with open("scenarios/features/fixtures/test.jpg", "rb") as f:
        bucket.put_object("test.jpg", body=f)
    context.res = bucket.image_process(key, action=query)


@then(u'image process status code is 200')
def step_impl(context):
    assert_that(context.res.status_code).is_equal_to(200)
    bucket.delete_object("test.jpg")
