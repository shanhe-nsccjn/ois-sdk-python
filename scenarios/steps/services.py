# -*- coding: utf-8 -*-

from os import path

from assertpy import assert_that
from behave import *

from ois.sdk.config import Config
from ois.sdk.service.ois import OIS

test_config_file_path = path.abspath(
    path.join(path.dirname(__file__), path.pardir)
)
config = Config(
).load_config_from_filepath(test_config_file_path + "/config.yaml")


@when(u'initialize OIS service')
def step_impl(context):
    context.ois = OIS(config)


@then(u'the OIS service is initialized')
def step_impl(context):
    assert_that(context.ois).is_not_none()


@when(u'list buckets')
def step_impl(context):
    context.ois = OIS(config)
    context.res = context.ois.list_buckets()


@then(u'list buckets status code is 200')
def step_impl(context):
    assert_that(context.res.status_code).is_equal_to(200)
