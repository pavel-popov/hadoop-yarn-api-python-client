# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import logging
import requests

from requests_kerberos import HTTPKerberosAuth

from .errors import APIError


# if this variable is not None then Kerberos authentication will be used
KRB = os.getenv('KRB5_REALM', None)


class Response(object):
    def __init__(self, json):
        self.data = json


class BaseYarnAPI(object):
    response_class = Response

    def request(self, api_path, **query_args):
        self.logger.info('Request http://%s:%s%s', self.address, self.port, api_path)
        
        auth = None if KRB is None else HTTPKerberosAuth()
        url = "http://{host}:{port}{path}".format(host=self.address, port=self.port, path=api_path)
        r = requests.get(url, params=query_args, auth=auth)
        
        if r.status_code == 200:
            return self.response_class(r.json())
        else:
            msg = 'Response finished with status: %s' % r.status_code
            raise APIError(msg)

    def construct_parameters(self, arguments):
        params = dict((key, value) for key, value in arguments if value is not None)
        return params

    __logger = None
    @property
    def logger(self):
        if self.__logger is None:
            self.__logger = logging.getLogger(self.__module__)
        return self.__logger
