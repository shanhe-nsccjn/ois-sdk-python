# +-------------------------------------------------------------------------
# | Copyright (C) 2021 shanhe, Inc.
# +-------------------------------------------------------------------------
# | Licensed under the Apache License, Version 2.0 (the "License");
# | you may not use this work except in compliance with the License.
# | You may obtain a copy of the License in the LICENSE file, or at:
# |
# | http://www.apache.org/licenses/LICENSE-2.0
# |
# | Unless required by applicable law or agreed to in writing, software
# | distributed under the License is distributed on an "AS IS" BASIS,
# | WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# | See the License for the specific language governing permissions and
# | limitations under the License.
# +-------------------------------------------------------------------------
# -*- coding: utf-8 -*-

from functools import partial

from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .bucket import Bucket
from ..request import Request
from ..unpack import Unpacker

# OIS provides OIS Service API (API Version 2021-01-06)


class OIS(object):

    def __init__(self, config):
        self.config = config
        self.client = Session()
        retries = Retry(
            total=self.config.connection_retries,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504]
        )
        self.client.mount(
            self.config.protocol + "://", HTTPAdapter(max_retries=retries)
        )
        if hasattr(self.config, "timeout") and self.config.timeout:
            self.client.send = partial(
                self.client.send, timeout=self.config.timeout
            )

    def list_buckets_request(self, limit=None, offset=None, location=None):
        operation = {
            "API": "ListBuckets",
            "Method": "GET",
            "URI": "/",
            "Headers": {},
            "Params": {
                "limit": limit,
                "offset": offset,
            },
            "Elements": {},
            "Properties": {},
            "Body": None
        }
        if location is not None:
            operation["Headers"]["Location"] = location
        self.list_buckets_validate(operation)
        return Request(self.config, operation)

    def list_buckets(self, limit=None, offset=None, location=None):
        req = self.list_buckets_request(
            limit=limit, offset=offset, location=location
        )
        resp = self.client.send(req.sign())
        return Unpacker(resp)

    @staticmethod
    def list_buckets_validate(op):
        pass

    def Bucket(self, bucket_name, zone):
        properties = {"bucket-name": bucket_name, "zone": zone}
        client = self.client
        return Bucket(self.config, properties, client)
